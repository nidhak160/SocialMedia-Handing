from django.db import models
from django.conf import settings
from posts.models import Post


class ScheduledPost(models.Model):
    STATUS = [
        ("pending", "Pending"),
        ("published", "Published"),
        ("failed", "Failed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )

    scheduled_time = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.caption[:30]
