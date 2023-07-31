import json
from rest_framework import status
from rest_framework.test import APITestCase
from contacts.models import Contact, ContactEmail, Note, NoteTypeChoices

URL = "/api/v2/contact/form/"
NAME = "Bob Jones"
EMAIL = "jones.bob@test.com"
MSG = "Hi, I was hoping for a trial lesson"
MSG2 = "Hi, this is a second message from Bob"
DATA = {
    "name": NAME,
    "contact_emails": [{"email": EMAIL}],
    "contact_notes": [{"note": MSG}],
}
DATA2 = {
    "name": NAME,
    "contact_emails": [{"email": EMAIL}],
    "contact_notes": [{"note": MSG2}],
}


class ContactFormTests(APITestCase):
    def test_create_contact(self):
        """
        Ensure we can create a new contact.
        """
        response = self.client.post(URL, DATA)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {"message": "ok"})
        self.assertEqual(Contact.objects.count(), 1)
        contact = Contact.objects.get(pk=1)
        self.assertEqual(contact.name, NAME)
        self.assertEqual(ContactEmail.objects.count(), 1)
        contact_email = ContactEmail.objects.get(pk=1)
        self.assertEqual(contact_email.email, EMAIL)
        self.assertEqual(contact_email.is_primary, True)
        self.assertEqual(contact_email.contact, contact)
        self.assertEqual(Note.objects.count(), 1)
        note = Note.objects.get(pk=1)
        self.assertEqual(note.contact, contact)
        self.assertEqual(note.title, "Email from jones.bob@test.com")
        self.assertEqual(note.note_type, 1)
        self.assertEqual(NoteTypeChoices.labels[note.note_type], "Email")
        self.assertEqual(note.note, MSG)

    def test_repeat_contact(self):
        """
        Ensure that a contact from a registered email will add note
        to contact notes.
        """
        response = self.client.post(URL, DATA)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(URL, DATA2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "ok"})
        self.assertEqual(Contact.objects.count(), 1)
        contact = Contact.objects.get(pk=1)
        self.assertEqual(Note.objects.count(), 2)
        note1 = Note.objects.get(pk=1)
        note2 = Note.objects.get(pk=2)
        self.assertEqual(note1.note, MSG)
        self.assertEqual(note2.note, MSG2)

    def test_error_on_no_email(self):
        """
        Ensure error if no email provided
        """
        data = {
            "name": NAME,
            "contact_emails": [{"email": ""}],
            "contact_notes": [{"note": MSG}],
        }
        response = self.client.post(URL, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.dumps(response.data),
            json.dumps({"email": ["This field may not be blank."]}),
        )

    def test_error_on_no_note(self):
        """
        Ensure error if no note provided
        """
        data = {
            "name": NAME,
            "contact_emails": [{"email": EMAIL}],
            "contact_notes": [{"note": ""}],
        }
        response = self.client.post(URL, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.dumps(response.data),
            json.dumps({"contact_notes": [{"note": ["This field may not be blank."]}]}),
        )
