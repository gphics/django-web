from django.urls import path
from .views import create_post

app_name = "chats"


urlpatterns = [
    path("create", create_post, name="create-post")
]
