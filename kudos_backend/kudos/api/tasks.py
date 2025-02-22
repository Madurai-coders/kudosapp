import logging
from celery import shared_task
from api.models import KudosQuota  # Ensure correct import

logger = logging.getLogger(__name__)

@shared_task(name="api.tasks.reset_kudos_task")  # Ensure the full name is correct
def reset_kudos_task():
    """Resets kudos_remaining to 3 every Sunday."""
    task_name = "Reset Kudos Task"  # Define a user-friendly name for logs
    
    updated_rows = KudosQuota.objects.update(kudos_remaining=3)  # Update all rows
    
    if updated_rows:
        logger.info(f"✅ {task_name}: Kudos Quota Reset to 3!")
    else:
        logger.warning(f"⚠️ {task_name}: No KudosQuota instances found!")
