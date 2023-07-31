from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.custom_permissions import SafeIPsPermission
from .models import Contact, ContactEmail
from .serializers import ContactFormSerializer, ContactFormEmailSerializer


class ContactFormView(APIView):
    """
    Write or Update view for contact form

    NOTE: Need IP Address permission class here
    """

    permission_classes = [SafeIPsPermission]

    def get_object(self, email):
        qs = ContactEmail.objects.filter(email__iexact=email)
        if qs.exists():
            contact_email = qs.first()
            contact = contact_email.contact
            return contact
        else:
            return None

    def post(self, request, format=None):
        email = None
        emails = request.data.get("contact_emails", [])
        if not len(emails):
            return Response(
                {"message": "must provide an email"}, status=status.HTTP_400_BAD_REQUEST
            )
        email_dict = emails[0]
        serializer = ContactFormEmailSerializer(data=email_dict)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        email = serializer.validated_data.get("email")
        contact = self.get_object(email)

        if not contact:
            # create new contact with new email and note
            serializer = ContactFormSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                # NOTE send alert email here
                return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            # update the relevant contact with new note
            # this is to bypass email unique validation, as we are not
            # saving an email this is ok
            request.data["contact_emails"][0]["email"] = f"REMOVE{email}"
            serializer = ContactFormSerializer(instance=contact, data=request.data)
            if serializer.is_valid():
                serializer.save()
                # NOTE send alert email here
                return Response({"message": "ok"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
