from django.db import models
from django.conf import settings


class Media(models.Model):
    MEDIA_TYPES = [
        ("image", "Image"),
        ("video", "Video"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    file = models.FileField(upload_to="media/")

    media_type = models.CharField(
        max_length=20,
        choices=MEDIA_TYPES
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name