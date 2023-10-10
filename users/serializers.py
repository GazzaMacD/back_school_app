from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from django.contrib.auth.models import Group

from contacts.serializers import ContactUserSerializer
from .models import CustomUser


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name",)


class CustomUserDetailsSerializer(UserDetailsSerializer):
    groups = GroupSerializer(many=True)
    contact = ContactUserSerializer()

    class Meta(UserDetailsSerializer.Meta):
        fields = (
            "email",
            "contact",
            "is_staff",
            "groups",
        )


class CustomUserContactNameSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="contact.name")

    class Meta:
        model = CustomUser
        fields = ("name",)
