from django.test import TestCase

from contacts.models import Contact, ContactEmail, Note
from django.contrib.auth import get_user_model

User = get_user_model()

USER1 = {
    "email": "user1@user.com",
    "password": "password",
}
USER2 = {
    "email": "user2@user.com",
    "password": "password",
}


class ContactModelTests(TestCase):
    # @classmethod
    # def setUpTestData(cls):
    #     cls.user1 = User.objects.create_user(**USER1)

    def test_contact_is_created_on_new_user_creation(self):
        self.assertEqual(Contact.objects.count(), 0)
        user2 = User.objects.create_user(**USER1)
        self.assertEqual(Contact.objects.count(), 1)

    def test_contact_is_related_to_user(self):
        user = User.objects.create_user(**USER1)
        contact = Contact.objects.first()
        self.assertEqual(contact, user.contact)

    def test_user_deletion_does_not_delete_contact(self):
        user1 = User.objects.create_user(**USER1)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(User.objects.count(), 1)
        user1.delete()
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Contact.objects.count(), 1)

    def test_contact_email_is_created_new_user_creation(self):
        self.assertEqual(ContactEmail.objects.count(), 0)
        user2 = User.objects.create_user(**USER1)
        contact = user2.contact
        self.assertEqual(ContactEmail.objects.count(), 1)
        email = ContactEmail.objects.first()
        self.assertEqual(contact, email.contact)
