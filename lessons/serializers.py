from rest_framework import serializers

from lessons.models import LessonCategory


class LessonCategorySerializer(serializers.ModelSerializer):
    """Read only serializer for categories"""

    class Meta:
        model = LessonCategory
        fields = ("id", "name", "ja_name", "slug")
