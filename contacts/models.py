from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from wagtail_headless_preview.models import HeadlessMixin
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.api import APIField

from core.models import TimeStampedModel
from users.models import CustomUser
from streams import customblocks


# ======== Contact Page ==========
class ContactPage(HeadlessMixin, Page):
    """Page for contact information as well as joining process"""

    ja_title = models.CharField(
        "Japanese Title",
        blank=False,
        null=False,
        max_length=15,
        help_text="Required. Max length 15 characters.",
    )
    short_intro = models.CharField(
        "Short Intro",
        blank=False,
        null=False,
        max_length=90,
        help_text="A  oneline introduction of what this page is about. Max length 90 chars",
    )
    assessment_trial = StreamField(
        [
            ("rich_text", customblocks.CustomRichTextBlock()),
            ("youtube", customblocks.YoutubeBlock()),
            ("info_cards", customblocks.InfoCardSeriesBlock()),
        ],
        use_json_field=True,
        null=True,
        blank=False,
    )
    join_experience = StreamField(
        [
            ("rich_text", customblocks.CustomRichTextBlock()),
            ("youtube", customblocks.YoutubeBlock()),
            ("info_cards", customblocks.InfoCardSeriesBlock()),
        ],
        use_json_field=True,
        null=True,
        blank=False,
    )
    question_and_answer = StreamField(
        [
            ("q_and_a", customblocks.QuestionAnswerSeriesBlock()),
        ],
        use_json_field=True,
        null=True,
        blank=False,
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("ja_title"),
                FieldPanel("short_intro"),
            ],
            heading="Contact page header area",
        ),
        MultiFieldPanel(
            [
                FieldPanel("assessment_trial"),
                FieldPanel("join_experience"),
                FieldPanel("question_and_answer"),
            ],
            heading="Contact page info section",
        ),
    ]

    # Api configuration
    api_fields = [
        APIField("ja_title"),
        APIField("short_intro"),
        APIField("assessment_trial"),
        APIField("join_experience"),
        APIField("question_and_answer"),
    ]

    max_count = 1
    parent_page_types = [
        "home.HomePage",
    ]

    def __str__(self):
        return self.title


# ======== Contact Model and associated models and logic ==========
class Contact(TimeStampedModel):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Only connect this to user IF a site user exists. Make sure that the email used for the user is registered in Contact emails as primary. This will generally be done by the system but in case manual connection is required, you can in this interface",
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

    def __str__(self) -> str:
        if self.name:
            return self.name
        elif self.user:
            return self.user.email
        else:
            return f"Anon User with id: {self.id}. Add name please."


@receiver(post_save, sender=CustomUser)
def create_or_update_contact(sender, instance, created, **kwargs):
    """Create new contact with 1-to-1 relation with newly created user or
    relate contact with same email address to new user. In case of update of user,
    check to see if mail is same as primary email of contact, if not update it to match
    """
    qs = ContactEmail.objects.filter(email__iexact=instance.email)
    if created:
        # new user so find if there is a contact entry
        # with the same email address. If so
        # connect them, and if not create a new contact
        # with an email registered as primary contact email
        if qs.exists():
            # contact with that email exists so conect them
            contact = qs.first().contact
            contact.user = instance
            contact.save()
        else:
            # No contact with that email found so create new contact
            # and new contact email with primary set as true
            contact = Contact(user=instance)
            contact.save()
            email = ContactEmail(contact=contact, is_primary=True, email=instance.email)
            email.save()
    else:
        # Updating a current user
        if qs.exists():
            connected_email = qs.first()
            contact = connected_email.contact
            # Set all this contacts mails is_primary to false
            contact_emails = ContactEmail.objects.filter(contact=contact)
            for email in contact_emails:
                # set all connected emals to false first
                email.is_primary = False
                email.save()
            # set this one to True
            connected_email.is_primary = True
            connected_email.save()
        else:
            # No email found so this must be a new email for this user
            # Set all other addresses for this user to be False
            contact_emails = ContactEmail.objects.filter(contact=instance.contact)
            for email in contact_emails:
                email.is_primary = False
                email.save()
            new_primary_email = ContactEmail(
                contact=instance.contact, is_primary=True, email=instance.email
            )
            new_primary_email.save()


class ContactEmail(TimeStampedModel):
    contact = models.ForeignKey(
        Contact,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name="contact_emails",
    )
    is_primary = models.BooleanField(
        _("Is primary"),
        blank=False,
        null=False,
        default=False,
    )
    email = models.CharField(
        _("Email"),
        unique=True,
        max_length=200,
        blank=False,
        null=False,
    )

    def __str__(self):
        return self.email


# ============= Notes ============
class NoteTypeChoices(models.IntegerChoices):
    REGULAR = 0, "Regular"
    EMAIL = 1, "Email"


class Note(TimeStampedModel):
    contact = models.ForeignKey(
        Contact,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="contact_notes",
    )
    title = models.CharField(
        _("title"),
        null=False,
        blank=False,
        max_length=50,
    )
    note_type = models.IntegerField(
        _("note type"),
        null=False,
        blank=False,
        default=NoteTypeChoices.REGULAR,
        choices=NoteTypeChoices.choices,
    )
    note = models.TextField(
        _("note"),
        null=False,
        blank=False,
    )

    def __str__(self) -> str:
        return self.title
