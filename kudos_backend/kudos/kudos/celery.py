import os
import logging
from celery import Celery
from celery.schedules import crontab

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set default Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kudos.settings")

app = Celery("kudos")

# Load config from settings.py using CELERY_ prefix
app.config_from_object("django.conf:settings", namespace="CELERY")

# Ensure timezone is set
app.conf.timezone = "UTC"  # Change as per your timezone (e.g., "America/New_York")

# Celery Beat Task Scheduling
app.conf.beat_schedule = {
    "reset-kudos-every-sunday-midnight": {
        "task": "api.tasks.reset_kudos_task",  # Ensure correct path
        "schedule": crontab(hour=0, minute=0, day_of_week="0"),  # Runs every Sunday at midnight
    },
}

# Auto-discover tasks in installed apps
app.autodiscover_tasks()

# Log Celery startup
logger.info("✅ Celery app configured successfully!")
