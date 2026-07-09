from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import ScheduledPost
from .serializers import ScheduledPostSerializer


class ScheduledPostView(generics.ListCreateAPIView):
    serializer_class = ScheduledPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ScheduledPost.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)