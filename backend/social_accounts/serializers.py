from rest_framework import serializers
from .models import SocialAccount


class SocialAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = SocialAccount
        fields = "__all__"
        read_only_fields = ["user"]