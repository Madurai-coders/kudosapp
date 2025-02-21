from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

class Organization(models.Model):
    name = models.CharField(max_length=255)

class Kudos(models.Model):
    giver = models.ForeignKey(User, related_name="kudos_given", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="kudos_received", on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class KudosQuota(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    kudos_remaining = models.IntegerField(default=3)
    last_reset = models.DateTimeField(default=now)

    def reset_quota(self):
        """Resets the kudos quota to 3 at the start of each week"""
        self.kudos_remaining = 3
        self.last_reset = now()
        self.save()