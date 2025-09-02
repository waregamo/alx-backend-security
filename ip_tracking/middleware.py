from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden
from django.core.cache import cache
from ip_tracking.models import RequestLog
try:
    from ip_tracking.models import BlockedIP
except ImportError:
    BlockedIP = None

from ipware import get_client_ip

GEO_TTL_SECONDS = 24 * 60 * 60  # 1 day


class IPTrackingMiddleware(MiddlewareMixin):
    """Logs IP, timestamp, path (and later: blocks + geolocation)."""

    def process_request(self, request):
        ip, _ = get_client_ip(request)
        if not ip:
            ip = "0.0.0.0"
        request._client_ip = ip  # stash for response phase

        # Task 1: BlockedIP check
        if BlockedIP is not None and BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Your IP has been blocked.")

    def process_response(self, request, response):
        ip = getattr(request, "_client_ip", None)
        if not ip:
            return response

        # Try reading cached geo
        geo = cache.get(f"geo:{ip}") or {}
        country = geo.get("country")
        city = geo.get("city")

        # If not cached, try django-ip-geolocation (its middleware put data on request.geolocation)
        if country is None and hasattr(request, "geolocation"):
            loc = request.geolocation
            # country is a dict: {"code": "KE", "name": "Kenya"} per package docs
            country = getattr(loc, "country", {}) or {}
            country = country.get("name")
            # city attribute may not be provided by all backends; be defensive
            city = getattr(loc, "city", None)

            cache.set(
                f"geo:{ip}",
                {"country": country, "city": city},
                timeout=GEO_TTL_SECONDS,
            )

        RequestLog.objects.create(
            ip_address=ip,
            path=getattr(request, "path", ""),
            country=country,
            city=city,
        )
        return response
