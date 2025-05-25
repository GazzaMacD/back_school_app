from rest_framework import serializers

from users.serializers import CustomUserContactNameSerializer
from .models import VideoCall


class VideoCallSerializer(serializers.ModelSerializer):
    teacher = CustomUserContactNameSerializer()

    class Meta:
        model = VideoCall
        fields = (
            "slug",
            "teacher",
            "host_room_url",
            "room_url",
        )
