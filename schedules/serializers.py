from rest_framework import serializers

from users.serializers import CustomUserContactNameSerializer
from languageschools.serializers import LanguageSchoolBasicSerializer
from .models import SuperSaasSchedule


class ScheduleSerializer(serializers.ModelSerializer):
    teacher = CustomUserContactNameSerializer()
    language_school = LanguageSchoolBasicSerializer()

    class Meta:
        model = SuperSaasSchedule
        fields = (
            "slug",
            "schedule_url",
            "teacher",
            "language_school",
        )
