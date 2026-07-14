from django.urls import path
from .views import (
    SocialAccountListCreateView,
    social_login,
    social_status,
)
from .facebook_views import (
    facebook_login,
    facebook_callback,
    share_post_to_facebook,
    facebook_status,
)
from .linkedin_views import linkedin_callback

urlpatterns = [
    path("", SocialAccountListCreateView.as_view(), name="social-accounts"),
    path("connect/<str:platform>/login/", social_login, name="social-login"),
    path("connect/<str:platform>/status/", social_status, name="social-status"),
    path("facebook/login/", facebook_login, name="facebook-login"),
    path("facebook/callback/", facebook_callback, name="facebook-callback"),
    path("facebook/status/", facebook_status, name="facebook-status"),
    path("facebook/share/<int:post_id>/", share_post_to_facebook, name="facebook-share"),
    path("linkedin/callback/", linkedin_callback, name="linkedin-callback"),
]
