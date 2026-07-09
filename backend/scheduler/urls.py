from django.urls import path
from .views import ScheduledPostView

urlpatterns = [
    path("", ScheduledPostView.as_view(), name="scheduler"),
]