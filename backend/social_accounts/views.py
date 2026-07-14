from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .facebook_views import get_facebook_login_url, facebook_settings_configured
from .linkedin_views import get_linkedin_login_url, linkedin_settings_configured
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
@permission_classes([AllowAny])
def social_login(request, platform):
    if platform == "facebook":
        if not facebook_settings_configured():
            return Response(
                {"error": "Facebook login is not configured."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        login_url = get_facebook_login_url()
        return Response({"login_url": login_url})

    if platform == "linkedin":
        if not linkedin_settings_configured():
            return Response(
                {"error": "LinkedIn login is not configured."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        login_url = get_linkedin_login_url()
        return Response({"login_url": login_url})

    return Response(
        {"error": f"OAuth login for {platform} is not yet implemented."},
        status=status.HTTP_501_NOT_IMPLEMENTED,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def social_status(request, platform):
    if platform == "facebook":
        try:
            social_account = SocialAccount.objects.get(
                user=request.user,
                platform="facebook",
                is_connected=True,
            )
            return Response(
                {
                    "is_connected": True,
                    "account_name": social_account.account_name,
                    "account_id": social_account.account_id,
                }
            )
        except SocialAccount.DoesNotExist:
            return Response({"is_connected": False})

    if platform == "linkedin":
        try:
            social_account = SocialAccount.objects.get(
                user=request.user,
                platform="linkedin",
                is_connected=True,
            )
            return Response(
                {
                    "is_connected": True,
                    "account_name": social_account.account_name,
                    "account_id": social_account.account_id,
                }
            )
        except SocialAccount.DoesNotExist:
            return Response({"is_connected": False})

    return Response(
        {
            "is_connected": False,
            "message": f"{platform} status not implemented yet.",
        }
    )
