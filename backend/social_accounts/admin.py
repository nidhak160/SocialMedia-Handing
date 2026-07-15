from django.contrib import admin
from .models import SocialAccount

@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "platform",
        "account_name",
        "page_name",
        "page_id",
        "is_connected",
    )