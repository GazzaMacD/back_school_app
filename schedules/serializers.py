from rest_framework import serializers

from .models import SuperSaasSchedule


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperSaasSchedule
        fields = ("slug", "schedule_url")
