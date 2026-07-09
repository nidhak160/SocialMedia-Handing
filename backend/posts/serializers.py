from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    content = serializers.CharField(source="caption", required=False, allow_blank=True)
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

    def validate(self, attrs):
        if not attrs.get("caption") and self.instance is None:
            raise serializers.ValidationError({
                "content": "Post content is required."
            })
        return attrs
