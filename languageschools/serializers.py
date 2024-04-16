from rest_framework import serializers

from .models import LanguageSchool


class LanguageSchoolBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageSchool
        fields = ("name",)
