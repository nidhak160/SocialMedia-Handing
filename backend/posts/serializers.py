import json
from rest_framework import serializers
from .models import Post
from social_accounts.serializers import SocialAccountSerializer

PLATFORM_CHOICES = [
    ("facebook", "Facebook"),
    ("instagram", "Instagram"),
    ("linkedin", "LinkedIn"),
    ("twitter", "X"),
    ("pinterest", "Pinterest"),
    ("threads", "Threads"),
]

class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=False, allow_blank=True)
    content = serializers.CharField(source="caption", required=False, allow_blank=True)
    platforms = serializers.JSONField(required=False)
    username = serializers.CharField(source="user.username", read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)
    social_accounts = SocialAccountSerializer(many=True, read_only=True)
    social_account_ids = serializers.CharField(
        write_only=True,
        required=False,
        help_text="JSON array of social account IDs"
    )

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
            "social_accounts",
            "social_account_ids",
            "image",
            "scheduled_time",
            "status",
            "created_at",
        ]
        read_only_fields = ["user", "username", "status", "created_at", "social_accounts"]
        extra_kwargs = {
            "caption": {"required": False, "allow_blank": True},
            "scheduled_time": {"required": False},
        }

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

    def validate_social_account_ids(self, value):
        # Handle JSON string from FormData
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except (json.JSONDecodeError, ValueError):
                raise serializers.ValidationError("Invalid JSON format for social account IDs.")
        
        if not isinstance(value, list):
            raise serializers.ValidationError("Social account IDs must be a list.")
        
        # Validate that all items are integers
        for item in value:
            if not isinstance(item, int):
                raise serializers.ValidationError(f"Invalid social account ID: {item}. Must be an integer.")
        
        return value

    def validate(self, attrs):
        if self.instance is None:
            caption = attrs.get("caption")
            title = attrs.get("title")
            image = attrs.get("image")
            if not caption and not title and not image:
                raise serializers.ValidationError({
                    "content": "Post content or image is required."
                })
        return attrs

    def create(self, validated_data):
        social_account_ids = validated_data.pop("social_account_ids", [])
        post = Post.objects.create(**validated_data)
        
        if social_account_ids:
            post.social_accounts.set(social_account_ids)
        
        return post

    def update(self, instance, validated_data):
        social_account_ids = validated_data.pop("social_account_ids", None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if social_account_ids is not None:
            instance.social_accounts.set(social_account_ids)
        
        return instance
