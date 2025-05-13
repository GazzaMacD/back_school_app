from rest_framework import serializers

from users.serializers import CustomUserContactNameSerializer
from .models import VideoCall


class VideoCallDetailSerializer(serializers.ModelSerializer):
    teacher = CustomUserContactNameSerializer()

    class Meta:
        model = VideoCall
        fields = (
            "slug",
            "teacher",
            "host_room_url",
            "room_url",
        )


class VideoCallListSerializer(serializers.ModelSerializer):
    teacher = CustomUserContactNameSerializer()

    class Meta:
        model = VideoCall
        fields = (
            "slug",
            "teacher",
        )
