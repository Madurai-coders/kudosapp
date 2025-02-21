from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import KudosQuota
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def create_kudos_quota(sender, instance, created, **kwargs):
    if created:
        KudosQuota.objects.create(user=instance)
