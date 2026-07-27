from django.urls import path
from .views import (
    SocialAccountListCreateView,
    SocialAccountDetailView,
    social_login,
    social_status,
)
from .facebook_views import (
    facebook_callback,
    share_post_to_facebook,
)
from .linkedin_views import (
    linkedin_callback,
    share_post_to_linkedin,
)

urlpatterns = [
    path("", SocialAccountListCreateView.as_view(), name="social-accounts"),
    path("<int:pk>/", SocialAccountDetailView.as_view(), name="social-account-detail"),

    path("connect/<str:platform>/login/", social_login, name="social-login"),
    path("facebook/callback/", facebook_callback, name="facebook-callback"),
    path("linkedin/callback/", linkedin_callback, name="linkedin-callback"),
    path("connect/<str:platform>/status/", social_status, name="social-status"),
    path("facebook/share/<int:post_id>/", share_post_to_facebook, name="facebook-share"),
    path("linkedin/share/<int:post_id>/", share_post_to_linkedin, name="linkedin-share"),
]