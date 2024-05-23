from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from core.custom_permissions import SafeIPsPermission
from .models import Contact, ContactEmail
from .serializers import ContactFormSerializer, ContactFormEmailSerializer


class ContactFormView(APIView):
    """
    Write or Update view for contact form

    NOTE: Permission checking domain name required here.
    """

    permission_classes = [AllowAny]

    def send_notification_email(self, email, validated_data):
        note = validated_data.get("contact_notes")[0].get("note")
        name = validated_data.get("name")
        name_en = validated_data.get("name_en")
        subject = f"IMPORTANT: {name} ({name_en}) contact via XLingual Contact Form "
        from_who = settings.EMAIL_HOST_USER
        to_who = settings.CONTACT_ALERT_EMAILS
        msg = (
            "Hi everyone,\n\n"
            "Please note that the following message has been submitted using the contact form.\n"
            f"\n----------    START   ----------\n\n"
            f"- {name}\n"
            f"- {name_en}\n"
            f"- {email}\n\n"
            f"---\n\n"
            f"{note}"
            f"\n\n----------     END    ----------\n\n"
            "This message should be in the CRM under this name or email. Please respond to the person as soon as possible.\n\n"
            "Thanks\n\n "
            "Xlingual Server"
        )
        send_mail(
            subject=subject,
            message=msg,
            from_email=from_who,
            recipient_list=to_who,
            fail_silently=False,
        )

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
                {"message": "Eメールアドレスを入力してください"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        email_dict = emails[0]
        email_serializer = ContactFormEmailSerializer(data=email_dict)
        if not email_serializer.is_valid():
            return Response(email_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        email = email_serializer.validated_data.get("email")
        contact = self.get_object(email)

        if not contact:
            # create new contact with new email and note
            serializer = ContactFormSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                # NOTE send alert email here with Celery if needed
                self.send_notification_email(email, serializer.validated_data)
                return Response({"details": "ok"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            # update the relevant contact with new note
            # REMOVE added to email
            # this is to bypass email unique validation, as we are not
            # saving an email this is ok
            request.data["contact_emails"][0]["email"] = f"REMOVE{email}"
            serializer = ContactFormSerializer(instance=contact, data=request.data)
            if serializer.is_valid():
                serializer.save()
                # NOTE send alert email here with Celery if needed
                self.send_notification_email(email, serializer.validated_data)
                return Response({"details": "ok"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
