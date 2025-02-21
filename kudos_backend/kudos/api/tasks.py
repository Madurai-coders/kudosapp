from celery import shared_task
from .models import KudosQuota  # Ensure correct import path
import logging

logger = logging.getLogger("cron")

@shared_task
def reset_kudos_task():
    """Alternates kudos_remaining between 0 and 3 every 2 minutes."""
    current_quota = KudosQuota.objects.first()  # Get first instance
    if current_quota and current_quota.kudos_remaining > 0:
        new_value = 0
    else:
        new_value = 3

    KudosQuota.objects.update(kudos_remaining=new_value)
    logger.info(f"✅ Kudos Quota Reset to {new_value}!")
