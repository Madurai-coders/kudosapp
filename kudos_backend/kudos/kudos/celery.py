import os
import django  # Ensure Django is set up before using models
from celery import Celery
from django.conf import settings
from django.db.models.signals import post_migrate
from django.dispatch import receiver

# Set default Django settings before setting up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kudos.settings")
django.setup()

app = Celery("kudos")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from installed Django apps
app.autodiscover_tasks()

# Ensure Celery uses Django's timezone
app.conf.timezone = settings.TIME_ZONE


# Register periodic task only after migrations are applied
@receiver(post_migrate)
def setup_periodic_tasks(sender, **kwargs):
    """Create the periodic task if it doesn't exist after migrations."""
    if sender.name == "django_celery_beat":  # Only run after this app's migrations
        from django_celery_beat.models import PeriodicTask, CrontabSchedule
        import json

        if not PeriodicTask.objects.filter(name="Reset Kudos").exists():
            schedule, _ = CrontabSchedule.objects.get_or_create(
                minute="0", hour="0", day_of_week="0", timezone="UTC"
            )

            PeriodicTask.objects.create(
                name="Reset Kudos",
                task="api.tasks.reset_kudos_task",
                crontab=schedule,
                args=json.dumps([]),
                enabled=True,
            )
