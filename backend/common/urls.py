from django.urls import path
from .views import privacy_policy, terms_of_service, data_deletion

urlpatterns = [
    path("privacy/", privacy_policy, name="privacy-policy"),
    path("terms/", terms_of_service, name="terms-of-service"),
    path("data-deletion/", data_deletion, name="data-deletion"),
]