# IP Tracking and Blocking System

A Django-based security application for monitoring, analyzing, and controlling access based on IP addresses.  
This project enhances application security by tracking incoming requests, enriching logs with geolocation data, blocking blacklisted IPs, applying rate limits, and detecting anomalies.

---

##  Features
- **IP Request Logging** – Record IP address, timestamp, country, city, and request path.  
- **IP Blacklisting** – Block malicious IPs via a custom Django management command.  
- **Geolocation Analytics** – Enrich request logs with geolocation data (country & city) using caching.  
- **Rate Limiting** – Prevent abuse with configurable request limits (via `django-ratelimit`).  
- **Anomaly Detection** – Automated Celery task flags suspicious IPs (e.g., >100 requests/hour or sensitive paths).  

---

## ⚙️Installation

1. **Clone the repository**  
   git clone https://github.com/waregamo/alx-backend-security.git
   cd alx-backend-security
## Create and activate a virtual environment


python3 -m venv .venv
source .venv/bin/activate
     Install dependencies
pip install -r requirements.txt
      Apply migrations
python manage.py makemigrations
python manage.py migrate
      Run the server
python manage.py runserver

## Usage
Visit any route → request logs will be automatically stored.

Block an IP:
python manage.py block_ip 127.0.0.1
A blocked IP visiting /login/ or any page will see:
Your IP has been blocked.

## Project Structure

alx-backend-security/
├── manage.py                     # Django entrypoint
├── alx_backend_security/         # Project settings
│   ├── settings.py               # Middleware, DB, installed apps
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── ip_tracking/                  # Custom security app
│   ├── models.py                 # RequestLog, BlockedIP, SuspiciousIP
│   ├── middleware.py             # IP logging & blocking
│   ├── tasks.py                  # Celery anomaly detection
│   ├── management/commands/      # Custom CLI (block_ip)
│   ├── migrations/               # DB migrations
│   ├── views.py                  # Views with rate limiting
│   ├── tests.py                  # Unit tests
│   └── admin.py                  # Django admin registration
├── db.sqlite3                    # Local SQLite database
├── requirements.txt
└── README.md

## 📌 Requirements
Python 3.8+
Django 4.x
django-ipware
django-ip-geolocation
django-ratelimit
Celery + Redis (for background anomaly detection tasks)