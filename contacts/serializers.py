from rest_framework import serializers

from .models import Contact


class ContactUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ("name",)
