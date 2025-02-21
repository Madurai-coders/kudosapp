from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import KudosQuota

@receiver(post_save, sender=User)
def create_kudos_quota(sender, instance, created, **kwargs):
    if created:
        KudosQuota.objects.create(user=instance)
