from django.db.models.signals import post_save,post_migrate
from django.dispatch import receiver
from .models import KudosQuota
from django.contrib.auth import get_user_model
import json

User = get_user_model()

@receiver(post_save, sender=User)
def create_kudos_quota(sender, instance, created, **kwargs):
    if created:
        KudosQuota.objects.create(user=instance)

@receiver(post_migrate)
def setup_periodic_tasks(sender, **kwargs):
    """Create the periodic task if it doesn't exist after migrations."""
    if sender.name == "django_celery_beat":  # Ensure it runs only for this app
        from django_celery_beat.models import PeriodicTask, CrontabSchedule  # Import inside function

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