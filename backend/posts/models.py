from django.db import models
from django.conf import settings
from django.utils import timezone


class Post(models.Model):
    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("posted", "Posted"),
        ("failed", "Failed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=255, blank=True, default="")
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to="posts/", blank=True, null=True)
    platforms = models.JSONField(default=list, blank=True)
    social_accounts = models.ManyToManyField(
        "social_accounts.SocialAccount",
        related_name="posts",
        blank=True,
    )
    scheduled_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="scheduled"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.title:
            return self.title
        return self.caption[:30]
