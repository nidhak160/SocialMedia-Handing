from rest_framework import serializers
from .models import SocialAccount


class SocialAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = SocialAccount
        fields = [
            "id",
            "platform",
            "account_name",
            "account_id",
            "is_connected",
            "connected_at",
            "updated_at",
        ]
        read_only_fields = ["id", "connected_at", "updated_at"]