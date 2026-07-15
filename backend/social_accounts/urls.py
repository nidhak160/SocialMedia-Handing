from django.urls import path
from .views import (
    SocialAccountListCreateView,
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
    # Social Accounts
    path(
        "",
        SocialAccountListCreateView.as_view(),
        name="social-accounts",
    ),

    # OAuth Login
    path(
        "connect/<str:platform>/login/",
        social_login,
        name="social-login",
    ),

    # OAuth Callback
    path(
        "facebook/callback/",
        facebook_callback,
        name="facebook-callback",
    ),

    path(
        "linkedin/callback/",
        linkedin_callback,
        name="linkedin-callback",
    ),

    # Connection Status
    path(
        "connect/<str:platform>/status/",
        social_status,
        name="social-status",
    ),

    # Publish Post
    path(
        "facebook/share/<int:post_id>/",
        share_post_to_facebook,
        name="facebook-share",
    ),

    path(
        "linkedin/share/<int:post_id>/",
        share_post_to_linkedin,
        name="linkedin-share",
    ),
]