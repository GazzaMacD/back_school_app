from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import VideoCall
from .serializers import VideoCallSerializer


class VideoCallListView(APIView):
    """Authenticated user only view for list view of all available teacher video calls"""

    # NOTE: Must remove comment here to lock down api
    permission_classes = [IsAuthenticated]

    def get(self, format=None):
        teachers = VideoCall.objects.all()
        serializer = VideoCallSerializer(teachers, many=True)
        return Response(serializer.data)
