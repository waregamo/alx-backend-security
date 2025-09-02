# IP Tracking and Blocking System

This Django project provides IP tracking and blocking functionality. It records request logs (IP, country, city, timestamp) and blocks blacklisted IP addresses from accessing the application.

---

## Features
- Track incoming requests with IP address, country, and city.
- Store request logs in the database.
- Block blacklisted IPs from accessing the system.
- Custom Django management command to block IPs.

---

## Installation

1. Clone the repository:
   git clone https://github.com/waregamo/alx-backend-security.git
   cd alx-backend-security

Create and activate a virtual environment:

python3 -m venv .venv
source .venv/bin/activate


Install dependencies:

pip install -r requirements.txt


Apply migrations:

python manage.py makemigrations
python manage.py migrate


Run the server:

python manage.py runserver

Usage

Visit any route in the app — request logs will be saved.

To block an IP:

python manage.py block_ip 127.0.0.1


When a blocked IP visits /login/, they will get:

Your IP has been blocked.
 

 Project structure
 alx-backend-security/
├── manage.py                 # Django entrypoint
├── alx_backend_security/                     # Main project settings
│   ├── settings.py           # Installed apps, DB, middleware, etc.
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── ip_tracking/              # Custom app
│   ├── models.py             # RequestLog, BlockedIP, SuspiciousIP
│   ├── middleware.py         # Blocks IPs on each request
│   ├── tasks.py              # Celery anomaly detection
│   ├── management/commands/  # Custom CLI (block_ip)
│   ├── migrations/           # DB migrations
│   ├── views.py
│   ├── tests.py
│   └── admin.py
├── db.sqlite3                # Local SQLite DB
├── requirements.txt
└── README.md
