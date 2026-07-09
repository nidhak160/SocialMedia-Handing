from django.urls import path
from .views import RegisterView, ProfileView, ProfileUpdateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    # Register
    path("register/", RegisterView.as_view()),

    # Login
    path("login/", TokenObtainPairView.as_view()),

    # Refresh Token
    path("refresh/", TokenRefreshView.as_view()),

    # Profile
    path("profile/", ProfileView.as_view()),

    # Profile Update
    path("profile/update/", ProfileUpdateView.as_view(), name="profile-update"),

]
