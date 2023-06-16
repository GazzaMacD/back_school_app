from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from django.contrib.auth.models import Group

from .models import CustomUser


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name",)


class CustomUserDetailsSerializer(UserDetailsSerializer):
    groups = GroupSerializer(many=True)

    class Meta(UserDetailsSerializer.Meta):
        fields = (
            "email",
            "full_name",
            "is_staff",
            "groups",
        )


class CustomUserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "full_name",
            "full_en_name",
        )
