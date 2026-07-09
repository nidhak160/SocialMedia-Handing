from django.db import models
from django.conf import settings


class SocialAccount(models.Model):
    PLATFORM_CHOICES = [
        ("facebook", "Facebook"),
        ("instagram", "Instagram"),
        ("linkedin", "LinkedIn"),
        ("twitter", "X (Twitter)"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="social_accounts"
    )

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    account_name = models.CharField(max_length=150)
    account_id = models.CharField(max_length=200, blank=True)
    access_token = models.TextField(blank=True)
    is_connected = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.platform}"