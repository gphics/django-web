from django.urls import path
from .views import MediaUploadView


app_name = "media"

urlpatterns = [
    path("", MediaUploadView.as_view(), name="upload")
]
