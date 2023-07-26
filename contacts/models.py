from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import TimeStampedModel
from users.models import CustomUser


class Contact(TimeStampedModel):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    name = models.CharField(
        _("name"),
        blank=True,
        null=False,
        max_length=100,
        help_text="Full name in the name order and language user would like. English or 日本語 for example. Max length: 100char",
    )
    name_en = models.CharField(
        _("english name"),
        blank=True,
        null=False,
        max_length=100,
        help_text="Full name in English, order should be same as name. Example 田中たろ should become Tanaka Taro in the field. Max length: 100char",
    )
    primary_email = models.EmailField(
        _("primary email address"),
        blank=True,
        null=False,
        unique=True,
        max_length=255,
        help_text="This email should be the same as for interacting with the site via the user model. Will be automatically updated if user changes via auth system",
    )

    def __str__(self) -> str:
        if self.name:
            return self.name
        return f"Anonymous Contact with ID: {self.pk}"


@receiver(post_save, sender=CustomUser)
def create_or_update_contact(sender, instance, created, **kwargs):
    """Create new contact with 1-to-1 relation with newly created user or
    relate contact with same email address to new user. In case of update of user,
    check to see if mail is same as primary email of contact, if not update it to match
    """
    qs = Contact.objects.filter(primary_email__iexact=instance.email)
    contact = None
    if created:
        if qs.exists():
            contact = qs.first()
            contact.user = instance
            return contact.save()
        else:
            contact = Contact(user=instance, primary_email=instance.email)
            return contact.save()
    elif (
        hasattr(instance, "contact")
        and instance.email != instance.contact.primary_email
    ):
        # The associated user has had their email changed so update
        # the primary_email field with the same email
        contact = Contact.objects.get(id=instance.contact.id)
        contact.primary_email = instance.email
        contact.save()
    else:
        pass
