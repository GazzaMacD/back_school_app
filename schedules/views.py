from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import SuperSaasSchedule
from .serializers import ScheduleSerializer


class ScheduleListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        schedules = SuperSaasSchedule.objects.all()
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)
