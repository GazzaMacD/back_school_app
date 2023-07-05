from django.shortcuts import render
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from lessons.models import LessonCategory
from lessons.serializers import LessonCategorySerializer


class LessonCategoryList(APIView):
    """
    List all lesson categories.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        snippets = LessonCategory.objects.all()
        serializer = LessonCategorySerializer(snippets, many=True)
        return Response(serializer.data)
