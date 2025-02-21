import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kudos.settings")

app = Celery("kudos")

# Load config from settings.py using CELERY_ prefix
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    "reset-kudos-every-2-mins": {
        "task": "api.tasks.reset_kudos_task",  # Ensure correct path
        "schedule": crontab(hour=0, minute=0, day_of_week="sunday"),  # Every Sunday at midnight

    },
}

# Auto-discover tasks in installed apps
app.autodiscover_tasks()
