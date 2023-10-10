from django.shortcuts import render
from django.http import JsonResponse, Http404

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import SuperSaasSchedule
from .serializers import ScheduleSerializer


class ScheduleListView(APIView):
    """Authenticated only list view for all supersass schedules"""

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        schedules = SuperSaasSchedule.objects.all()
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)


class ScheduleDetailView(APIView):
    """Authenticated only single supersaas schedule using slug"""

    permission_classes = [IsAuthenticated]

    def get_object(self, slug):
        try:
            schedule_obj = SuperSaasSchedule.objects.get(slug=slug)
            return schedule_obj
        except SuperSaasSchedule.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        schedule = self.get_object(slug)
        serializer = ScheduleSerializer(schedule)
        return Response(serializer.data)
