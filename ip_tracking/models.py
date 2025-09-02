from django.db import models


class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField()
    path = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    country = models.CharField(max_length=64, blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["ip_address", "timestamp"]),
            models.Index(fields=["path", "timestamp"]),
        ]
        ordering = ["-timestamp"]  # Optional: show latest logs first

    def __str__(self):
        return f"{self.ip_address} - {self.path} @ {self.timestamp:%Y-%m-%d %H:%M:%S}"


class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    reason = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]  # Optional: newest blocked IPs first

    def __str__(self):
        return f"{self.ip_address} (Blocked: {self.created_at:%Y-%m-%d %H:%M:%S})"


class SuspiciousIP(models.Model):
    ip_address = models.GenericIPAddressField()
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["ip_address", "created_at"])]

    def __str__(self):
        return f"{self.ip_address} ({self.reason})"
