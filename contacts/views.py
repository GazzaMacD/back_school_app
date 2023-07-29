from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Contact, ContactEmail
from .serializers import ContactFormSerializer


class ContactFormView(APIView):
    """
    Write or Update view for contact form

    NOTE: Need IP Address permission class here
    """

    permission_classes = [AllowAny]

    def get_object(self, email):
        qs = ContactEmail.objects.filter(email__iexact=email)
        if qs.exists():
            contact_email = qs.first()
            contact = contact_email.contact
            return contact
        else:
            return None

    def post(self, request, format=None):
        email = request.data["contact_emails"][0]["email"]
        email = self.get_object(email)
        if not email:
            # create new contact with new email and note
            data = {"name": request.data["name"]}
            serializer = ContactFormSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return JsonResponse(
                {"message": "ERROR"}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            # update the relevant contact with new note
            return JsonResponse({"message": "Updated"}, status=200)
