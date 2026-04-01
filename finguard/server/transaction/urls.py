from django.urls import path
from .views import (CategoryCRUDView, TransactionCRUDView, CircleCRUDView, add_circle_member,remove_circle_member, interpret_summary_statistics, leave_circle, rank_circle_members
    )


app_name = "transaction"

urlpatterns = [
     # Transaction
    path("interpret", interpret_summary_statistics, name="interpret-transaction"),
    path("add-circle-member/<int:id>", add_circle_member, name="add-circle-member"),
    path("remove-circle-member/<int:id>", remove_circle_member, name="remove-circle-member"),
    path("leave-circle/<int:id>",leave_circle, name="leave-circle"),
    path("rank-circle-members/<int:id>",rank_circle_members, name="rank-circle-members"),
     
    # 
    # Class based views
    path("category", CategoryCRUDView.as_view(), name="category"),
    path("", TransactionCRUDView.as_view(), name="transaction"),
    path("circle", CircleCRUDView.as_view(), name="circle"),
]
