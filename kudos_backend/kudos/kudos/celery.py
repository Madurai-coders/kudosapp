# import os
# import logging
# from celery import Celery
# from celery.schedules import crontab

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Set default Django settings
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kudos.settings")

# app = Celery("kudos")

# # Load config from settings.py using CELERY_ prefix
# app.config_from_object("django.conf:settings", namespace="CELERY")

# # Ensure timezone is set
# app.conf.timezone = "UTC"  # Change as per your timezone (e.g., "America/New_York")

# # Celery Beat Task Scheduling
# app.conf.beat_schedule = {
#     "reset-kudos-every-sunday-midnight": {
#         "task": "api.tasks.reset_kudos_task",  # Ensure correct path
#         # "schedule": crontab(hour=0, minute=0, day_of_week="0"),  # Runs every Sunday at midnight
#         "schedule": crontab(minute="*/2")
#     },
# }

# # Auto-discover tasks in installed apps
# app.autodiscover_tasks()


import os
import django  # Ensure Django is set up before using models
from celery import Celery

# Set default Django settings before setting up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kudos.settings")
django.setup()

app = Celery("kudos")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from installed Django apps
app.autodiscover_tasks()

# Ensure Celery uses Django's timezone
from django.conf import settings
app.conf.timezone = settings.TIME_ZONE

# Register periodic task on Celery start
def setup_periodic_tasks():
    """Create the periodic task if it doesn't exist."""
    from django_celery_beat.models import PeriodicTask, CrontabSchedule
    import json

    if not PeriodicTask.objects.filter(name="Reset Kudos").exists():
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute="0",        # At the start of the hour (minute 0)
            hour="0",          # At midnight (hour 0)
            day_of_week="0",   # Sunday (0 is Sunday, 1 is Monday, ..., 6 is Saturday)
            timezone="UTC"     # Use your desired timezone (e.g., "UTC", "America/New_York")
        )


        PeriodicTask.objects.create(
            name="Reset Kudos",
            task="api.tasks.reset_kudos_task",
            crontab=schedule,
            args=json.dumps([]),
            enabled=True,
        )

# Run periodic task setup when Celery starts
setup_periodic_tasks()
