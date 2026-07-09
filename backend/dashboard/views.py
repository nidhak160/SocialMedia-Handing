from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Dashboard
from .serializers import DashboardSerializer

# Create your views here.

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        dashboard, created = Dashboard.objects.get_or_create(user=request.user)

        serializer = DashboardSerializer(dashboard)

        return Response(serializer.data)