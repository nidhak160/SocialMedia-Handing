from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import SocialAccount
from .serializers import SocialAccountSerializer


class SocialAccountListCreateView(generics.ListCreateAPIView):

    serializer_class = SocialAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SocialAccount.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)