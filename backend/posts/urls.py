from django.urls import path
from .views import PostDetailView, PostListCreateView

urlpatterns = [
    path("", PostListCreateView.as_view()),
    path("<int:pk>/", PostDetailView.as_view()),
]
