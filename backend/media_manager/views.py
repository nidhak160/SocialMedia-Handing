from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Media
from .serializers import MediaSerializer


class MediaListCreateView(generics.ListCreateAPIView):
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Media.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)