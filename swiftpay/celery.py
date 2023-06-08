# django_celery/celery.py

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swiftpay.settings")
app = Celery("swiftpay")
app.config_from_object("django.conf:settings", namespace="swiftpay")
app.autodiscover_tasks()