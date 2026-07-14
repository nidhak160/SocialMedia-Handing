from rest_framework import serializers
from .models import Post

PLATFORM_CHOICES = [
    ("facebook", "Facebook"),
    ("instagram", "Instagram"),
    ("linkedin", "LinkedIn"),
    ("twitter", "X"),
    ("pinterest", "Pinterest"),
    ("threads", "Threads"),
]

class PostSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    content = serializers.CharField(source="caption", required=False, allow_blank=True)
    platforms = serializers.JSONField(required=False)
    username = serializers.CharField(source="user.username", read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "username",
            "title",
            "content",
            "caption",
            "platforms",
            "image",
            "scheduled_time",
            "status",
            "created_at",
        ]
        read_only_fields = ["user", "username", "title", "status", "created_at"]
        extra_kwargs = {
            "caption": {"required": False, "allow_blank": True},
            "scheduled_time": {"required": False},
        }

    def get_title(self, obj):
        return obj.caption[:80]

    def validate_platforms(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Platforms must be a list.")

        valid_platforms = [choice[0] for choice in PLATFORM_CHOICES]
        invalid = [item for item in value if item not in valid_platforms]
        if invalid:
            raise serializers.ValidationError(
                f"Unsupported platforms: {', '.join(invalid)}"
            )
        return value

    def validate(self, attrs):
        if self.instance is None:
            caption = attrs.get("caption")
            image = attrs.get("image")
            if not caption and not image:
                raise serializers.ValidationError({
                    "content": "Post content or image is required."
                })
        return attrs
