from rest_framework import serializers

from users.serializers import CustomUserBasicContactSerializer
from languageschools.serializers import LanguageSchoolBasicSerializer
from .models import SuperSaasSchedule


class ScheduleSerializer(serializers.ModelSerializer):
    teacher = CustomUserBasicContactSerializer()
    language_school = LanguageSchoolBasicSerializer()

    class Meta:
        model = SuperSaasSchedule
        fields = (
            "slug",
            "schedule_url",
            "teacher",
            "language_school",
        )
