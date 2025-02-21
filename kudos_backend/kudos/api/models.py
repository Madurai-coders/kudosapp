from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):  # Custom User model
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.username


class Kudos(models.Model):
    giver = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="kudos_given", on_delete=models.CASCADE, db_index=True
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="kudos_received", on_delete=models.CASCADE, db_index=True
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                check=~models.Q(giver=models.F("receiver")),
                name="prevent_self_kudos",
            )
        ]

    def __str__(self):
        return f"Kudos from {self.giver} to {self.receiver}"


class KudosQuota(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    kudos_remaining = models.PositiveIntegerField(default=3)
    last_reset = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} - {self.kudos_remaining} kudos left"
