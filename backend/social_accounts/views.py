from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .services.facebook_service import (
    facebook_settings_configured as facebook_service_configured,
    get_facebook_login_url,
)
from .services.linkedin_service import (
    linkedin_settings_configured as linkedin_service_configured,
    get_linkedin_login_url,
)
from .models import SocialAccount
from .serializers import SocialAccountSerializer


class SocialAccountListCreateView(generics.ListCreateAPIView):

    serializer_class = SocialAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SocialAccount.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def social_login(request, platform):
    if platform == "facebook":
        if not facebook_service_configured():
            return Response(
                {"error": "Facebook login is not configured."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        login_url = get_facebook_login_url(request.user)
        return Response({"login_url": login_url})

    if platform == "linkedin":
        if not linkedin_service_configured():
            return Response(
                {"error": "LinkedIn login is not configured."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        login_url = get_linkedin_login_url(request.user)
        return Response({"login_url": login_url})

    return Response(
        {"error": f"OAuth login for {platform} is not yet implemented."},
        status=status.HTTP_501_NOT_IMPLEMENTED,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def social_status(request, platform):
    social_account = SocialAccount.objects.filter(
        user=request.user,
        platform=platform,
        is_connected=True,
    ).first()

    if not social_account:
        return Response({"is_connected": False})

    return Response(
        {
            "is_connected": True,
            "account_name": social_account.account_name,
            "account_id": social_account.account_id,
        }
    )
