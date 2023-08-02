from rest_framework import serializers

from .models import Contact, ContactEmail, Note


class ContactUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ("name",)


# Contact Form Serializers


class ContactFormEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_blank=False, max_length=200)


class ContactFormContactEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactEmail
        fields = ("email",)


class ContactFormNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ("note",)


class ContactFormSerializer(serializers.ModelSerializer):
    contact_emails = ContactFormContactEmailSerializer(many=True)
    contact_notes = ContactFormNoteSerializer(many=True)

    class Meta:
        model = Contact
        fields = ("name", "name_en", "contact_emails", "contact_notes")

    def create(self, validated_data):
        email_data = validated_data.pop("contact_emails")
        note_data = validated_data.pop("contact_notes")
        contact = Contact.objects.create(**validated_data)
        contact_email = None
        for email in email_data:
            email_dict = dict(email)
            email_dict["is_primary"] = True
            contact_email = email_dict["email"]
            ContactEmail.objects.create(contact=contact, **email_dict)
        for note in note_data:
            note_dict = dict(note)
            note_dict["note_type"] = 1
            note_dict["title"] = f"Email from {contact_email}"
            Note.objects.create(contact=contact, **note_dict)
        return contact

    def update(self, instance, validated_data):
        email_data = validated_data.pop("contact_emails")
        note_data = validated_data.pop("contact_notes")
        contact_email = None
        for email in email_data:
            email_dict = dict(email)
            contact_email = email_dict["email"]
            contact_email = contact_email[6:]  # remove 'REMOVE"
        for note in note_data:
            note_dict = dict(note)
            note_dict["note_type"] = 1
            note_dict["title"] = f"Email from {contact_email}"
            Note.objects.create(contact=instance, **note_dict)
        return instance
