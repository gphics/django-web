from django.urls import path
from .views import (create_user, auth_user, ProvileView, update_email, update_username, update_password,  get_currencies)

app_name = "account"
 
urlpatterns = [
    path("reg", create_user, name="reg"),
    path("auth", auth_user, name="auth"),
    path("update-email", update_email, name="update-email"),
    path("update-username", update_username, name="update-username"),
    path("update-password", update_password, name="update-password"),
    path("profile/currencies", get_currencies, name="all-currencies"),


    # Class based view
    path("profile", ProvileView.as_view(), name="profile"),
]
