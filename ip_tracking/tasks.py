# ip_tracking/tasks.py
from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from django.db.models import Count
from .models import RequestLog, SuspiciousIP

SENSITIVE_PATHS = {"/admin", "/login", "/accounts/login/"}

@shared_task
def detect_anomalies():
    now = timezone.now()
    since = now - timedelta(hours=1)

    # 1) High-volume offenders
    hot = (
        RequestLog.objects.filter(timestamp__gte=since)
        .values("ip_address")
        .annotate(n=Count("id"))
        .filter(n__gt=100)
    )
    for row in hot:
        SuspiciousIP.objects.get_or_create(
            ip_address=row["ip_address"],
            reason=f"High volume: {row['n']} requests in last hour",
        )

    # 2) Sensitive paths touched
    sens_ips = (
        RequestLog.objects.filter(timestamp__gte=since, path__in=SENSITIVE_PATHS)
        .values_list("ip_address", flat=True)
        .distinct()
    )
    for ip in sens_ips:
        SuspiciousIP.objects.get_or_create(
            ip_address=ip,
            reason="Accessed sensitive paths",
        )
