import html
import re
import string

from django.core.mail import send_mail
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from .models import ContactEmail, BannedEmail
from .serializers import (
    ContactFormSerializer,
    ContactFormEmailSerializer,
    BannedEmailSerializer,
)


class ContactFormView(APIView):
    """
    Write or Update view for contact form

    NOTE: Permission checking domain name required here.
    """

    permission_classes = [AllowAny]

    def ascii_percentage_analysis(self, s, per):
        """Function to analyze if a string contains mostly ascii strings by percentage.
        Will take the string to analyse and a percentage integer and return True if over
        percentage and False if below.
        """
        # change string to set to get 0(1)
        test_set = set(string.ascii_letters + string.whitespace + string.punctuation)
        total_char = 0
        total_ascii = 0
        per = int(per)
        for char in s:
            total_char += 1
            if char in test_set:
                total_ascii += 1
        return (total_ascii / total_char) * 100 > per

    def send_notification_email(self, email, validated_data):
        note = validated_data.get("contact_notes")[0].get("note")
        # Sanitize note:
        # Remove any html in the text
        # Reduce note to accepted max 300 chars
        # Remove all links
        note = re.sub(
            r"(https?:\/\/)(\s)*(www\.)?(\s)*((\w|\s)+\.)*([\w\-\s]+\/)*([\w\-]+)((\?)?[\w\s]*=\s*[\w\%&]*)*",
            " **removed link** ",
            html.escape(note)[0:300],
        )
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
        try:
            send_mail(
                subject=subject,
                message=msg,
                from_email=from_who,
                recipient_list=to_who,
                fail_silently=False,
            )

        except Exception as e:
            raise e

    def get_object(self, email):
        qs = ContactEmail.objects.filter(email__iexact=email)
        if qs.exists():
            contact_email = qs.first()
            contact = contact_email.contact
            return contact
        else:
            return None

    def post(self, request, format=None):
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
        email = email_serializer.validated_data.get("email", None)
        if email:
            email = email.strip()

        # =========== Deal with Junk here ============
        # 1. Check to see if email in banned emails, if yes return 422 to front
        # NOTE This code is valid while we consider that we are only getting contact mails in Japanese.
        # A new strategy will be needed when the emails are for Japanese lessons.
        # 2. Check to see if email contains too much english. For now (2025.01) probably junk so.
        #   2.1 If yes then save the details in banned emails along with mail for future junk analysis purposes.

        if BannedEmail.objects.filter(email__iexact=email).exists():
            return Response(
                {"message": "banned email"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        # get msg
        notes = request.data.get("contact_notes", [])
        if not len(notes):
            return Response(
                {"message": "banned email"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        else:
            message_dict = notes[0]
            if self.ascii_percentage_analysis(message_dict["note"], 60):
                name = request.data.get("name")
                data = {"name": name, "email": email, "message": message_dict["note"]}
                banned_email_serializer = BannedEmailSerializer(data=data)
                if banned_email_serializer.is_valid():
                    banned_email_serializer.save()
                # In both is_valid() and not valid case use, 422
                return Response(
                    {"message": "banned email"},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )
            else:
                pass
        # Now get the contact if any, associated with this mail
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
                try:
                    self.send_notification_email(email, serializer.validated_data)
                except Exception as e:
                    print(e)
                    return Response(
                        {"message": "Send mail failed for some reason"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

                return Response({"details": "ok"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
