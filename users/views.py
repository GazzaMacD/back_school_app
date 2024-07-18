import html

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

from contacts.serializers import GetUpdateContactSerializer
from contacts.models import Contact

# Get the current UserModel
UserModel = get_user_model()


class GetUpdateContactView(APIView):
    """
    Get current contact names and have option to update them
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return UserModel.objects.get(pk=pk).contact
        except UserModel.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        contact = self.get_object(pk)
        serializer = GetUpdateContactSerializer(contact)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        contact = self.get_object(pk)
        serializer = GetUpdateContactSerializer(contact, data=request.data)
        if serializer.is_valid():
            # Sanitize string
            serializer.validated_data.update(
                {
                    "name": html.escape(serializer.validated_data.get("name")),
                    "name_en": html.escape(serializer.validated_data.get("name_en")),
                }
            )
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
