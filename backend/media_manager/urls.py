from django.urls import path
from .views import MediaListCreateView

urlpatterns = [
    path("", MediaListCreateView.as_view(), name="media"),
]