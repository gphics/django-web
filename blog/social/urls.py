from django.urls import path
from .views import post_detail, post_list,create_comment

app_name = "social"

urlpatterns = [
    path("", post_list, name="post_list"),
    path("<int:year>/<int:month>/<int:day>/<slug:post>", post_detail, name="post_detail"),
    path("post/<int:post_id>", create_comment, name="create_comment")

]
