from django.urls import path
from .views import SocialAccountListCreateView
from .facebook_views import (
    facebook_login,
    facebook_callback,
    share_post_to_facebook,
    facebook_status,
)

urlpatterns = [
    path("", SocialAccountListCreateView.as_view(), name="social-accounts"),
    path("facebook/login/", facebook_login, name="facebook-login"),
    path("facebook/callback/", facebook_callback, name="facebook-callback"),
    path("facebook/status/", facebook_status, name="facebook-status"),
    path("facebook/share/<int:post_id>/", share_post_to_facebook, name="facebook-share"),
]
