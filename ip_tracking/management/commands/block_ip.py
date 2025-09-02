
from django.core.management.base import BaseCommand, CommandError
from ip_tracking.models import BlockedIP

class Command(BaseCommand):
    help = "Add an IP to BlockedIP"

    def add_arguments(self, parser):
        parser.add_argument("ip_address", type=str, help="IP to block")
        parser.add_argument("--reason", type=str, default="", help="Reason")

    def handle(self, *args, **opts):
        ip = opts["ip_address"].strip()
        reason = opts["reason"]
        obj, created = BlockedIP.objects.get_or_create(ip_address=ip, defaults={"reason": reason})
        if not created and reason and obj.reason != reason:
            obj.reason = reason
            obj.save(update_fields=["reason"])
        self.stdout.write(self.style.SUCCESS(f"Blocked {ip}"))
