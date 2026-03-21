from django.urls import path
from .views import (
    create_user, auth_user, ProvileView, update_email, update_username, update_password,CategoryCRUDView, TransactionCRUDView, CircleCRUDView, add_circle_member,remove_circle_member, tranaction_deep_dive, get_all_currencies, interpret_summary_statistics
    )



app_name = "main"


urlpatterns = [

    # 
    #  User and Profile
    path("reg", create_user, name="reg"),
    path("auth", auth_user, name="auth"),
    path("update-email", update_email, name="update-email"),
    path("update-username", update_username, name="update-username"),
    path("update-password", update_password, name="update-password"),
    path("profile/all-currencies", get_all_currencies, name="all-currencies"),


    # 
    # Transaction
    path("transaction/deep", tranaction_deep_dive, name="deep-transaction"),
    path("transaction/interpret", interpret_summary_statistics, name="interpret-transaction"),
    path("add-circle-member/<int:id>", add_circle_member, name="add-circle-member"),
    path("add-circle-member/<int:id>", remove_circle_member, name="remove-circle-member"),
    
    # 
    # Class based views
    path("profile", ProvileView.as_view(), name="profile"),
    path("category", CategoryCRUDView.as_view(), name="category"),
    path("transaction", TransactionCRUDView.as_view(), name="transaction"),
    path("circle", CircleCRUDView.as_view(), name="circle"),
]
