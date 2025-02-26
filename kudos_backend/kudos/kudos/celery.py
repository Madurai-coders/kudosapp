import os
import django  # Ensure Django is set up before using models
from celery import Celery
from django.conf import settings


# Set default Django settings before setting up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kudos.settings")
django.setup()

app = Celery("kudos")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from installed Django apps
app.autodiscover_tasks()

# Ensure Celery uses Django's timezone
app.conf.timezone = settings.TIME_ZONE


