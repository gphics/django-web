from rest_framework import serializers
from .models import Media

class MediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Media
        # fields = "__all__"
        exclude = ["user_profile", "circle"]