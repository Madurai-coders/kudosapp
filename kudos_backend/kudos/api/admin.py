from django.contrib import admin
from .models import Kudos,KudosQuota

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