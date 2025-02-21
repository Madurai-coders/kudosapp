from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Kudos, KudosQuota, User  # Import your custom User model

@admin.register(User)
class CustomUserAdmin(UserAdmin):  
    list_display = ("id", "username", "email", "organization", "is_staff", "is_active")
    search_fields = ("username", "email", "organization__name")
    list_filter = ("is_staff", "is_active", "organization")
    ordering = ("id",)

@admin.register(Kudos)
class KudosAdmin(admin.ModelAdmin):
    list_display = ("id", "giver", "receiver", "message", "created_at")
    search_fields = ("giver__username", "receiver__username", "message")
    list_filter = ("created_at",)
    ordering = ("-created_at",)

@admin.register(KudosQuota)
class KudosQuotaAdmin(admin.ModelAdmin):
    list_display = ("user", "kudos_remaining", "last_reset")
    search_fields = ("user__username",)
    ordering = ("user",)
