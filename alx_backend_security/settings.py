
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret")
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "ip_tracking",            
    # 'django_ratelimit' is decorator-based; no need to add to INSTALLED_APPS
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    # Geolocation middleware must run BEFORE our logger so request.geolocation is available
    "django_ip_geolocation.middleware.IpGeolocationMiddleware",  # :contentReference[oaicite:3]{index=3}
    "ip_tracking.middleware.IPTrackingMiddleware",
]

ROOT_URLCONF = "alx_backend_security.urls"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.debug",
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]
WSGI_APPLICATION = "alx_backend_security.wsgi.application"

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3",
                         "NAME": BASE_DIR / "db.sqlite3"}}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Nairobi"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"

# Cache (used for geo lookups + ratelimit counters)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "ip-tracking-cache",
    }
}

# django-ratelimit uses Django cache
RATELIMIT_USE_CACHE = "default"   # :contentReference[oaicite:4]{index=4}

# django-ip-geolocation settings (defaults are fine; shown for clarity)
IP_GEOLOCATION_SETTINGS = {
    "BACKEND": "django_ip_geolocation.backends.IPGeolocationAPI",  # no API key needed for demo
    "ENABLE_REQUEST_HOOK": True,
    "ENABLE_RESPONSE_HOOK": False,
}

# Celery (Redis broker)
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_TIMEZONE = TIME_ZONE

from celery.schedules import crontab
CELERY_BEAT_SCHEDULE = {
    "detect-anomalies-hourly": {
        "task": "ip_tracking.tasks.detect_anomalies",
        "schedule": crontab(minute=0),  # hourly at minute :00
    }
}
