from django.db import models
from django.conf import settings

class Dashboard(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    total_posts = models.IntegerField(default=0)
    scheduled_posts = models.IntegerField(default=0)
    draft_posts = models.IntegerField(default=0)
    connected_accounts = models.IntegerField(default=0)

    def __str__(self):
        return self.user.email