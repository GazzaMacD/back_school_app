from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from wagtail_headless_preview.models import HeadlessMixin
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.api import APIField
from wagtail.fields import RichTextField

from core.models import TimeStampedModel
from users.models import CustomUser
from streams import customblocks


# ======== Contact Page ==========
class ContactPage(HeadlessMixin, Page):
    """Page for contact information as well as joining process"""

    # Header section
    display_title = models.CharField(
        "Display Title",
        blank=False,
        null=False,
        max_length=15,
        help_text="Required. Max length 15 characters. Japanese",
    )
    # Trial lesson section
    trial_en_title = models.CharField(
        "Trial - English Title",
        blank=False,
        null=False,
        max_length=25,
        help_text="Required. Max length 25, 15 or less is ideal",
    )
    trial_jp_title = models.CharField(
        "Trial - Japanese Title",
        blank=False,
        null=False,
        max_length=20,
        help_text="Required. Max length 20 characters, 15 or less is ideal",
    )
    trial_intro = RichTextField(
        "Trial - Intro",
        features=["bold", "link"],
    )
    trial_steps = StreamField(
        [
            ("info_cards", customblocks.InfoCardBlockOptionalPic()),
        ],
        use_json_field=True,
        null=True,
        blank=False,
    )

    # Learning experiences section
    exp_en_title = models.CharField(
        "Learning Experiences - English Title",
        blank=False,
        null=False,
        max_length=25,
        help_text="Required. Max length 25, 15 or less is ideal",
    )
    exp_jp_title = models.CharField(
        "Learning Experiences - Japanese Title",
        blank=False,
        null=False,
        max_length=20,
        help_text="Required. Max length 20 characters, 15 or less is ideal",
    )
    exp_intro = RichTextField(
        "Learning Experiences - Intro",
        features=["bold", "link"],
    )
    exp_steps = StreamField(
        [
            ("info_cards", customblocks.InfoCardBlockOptionalPic()),
        ],
        use_json_field=True,
        null=True,
        blank=False,
    )

    # Q & A section
    qa_en_title = models.CharField(
        "Q & A - English Title",
        blank=False,
        null=False,
        max_length=25,
        help_text="Required. Max length 25, 15 or less is ideal",
    )
    qa_jp_title = models.CharField(
        "Q & A - Japanese Title",
        blank=False,
        null=False,
        max_length=20,
        help_text="Required. Max length 20 characters, 15 or less is ideal",
    )
    qas = StreamField(
        [
            ("q_and_a", customblocks.QuestionAnswerBlock()),
        ],
        use_json_field=True,
        null=True,
        blank=False,
    )

    # Telephone section
    tel_en_title = models.CharField(
        "Telephone - English Title",
        blank=False,
        null=False,
        max_length=25,
        help_text="Required. Max length 25, 15 or less is ideal",
    )
    tel_jp_title = models.CharField(
        "Telephone - Japanese Title",
        blank=False,
        null=False,
        max_length=20,
        help_text="Required. Max length 20 characters, 15 or less is ideal",
    )
    tel_number = models.CharField(
        "Telephone - Actual Number",
        blank=False,
        null=False,
        max_length=20,
        help_text="Required. No spaces! Max length 20 characters, 15 or less is ideal",
    )
    tel_display_number = models.CharField(
        "Telephone - Display Number",
        blank=False,
        null=False,
        max_length=20,
        help_text="Required. Hyphens and spaces ok for readability! Max length 20 characters, 15 or less is ideal",
    )

    # Form section
    form_en_title = models.CharField(
        "Form - English Title",
        blank=False,
        null=False,
        max_length=25,
        help_text="Required. Max length 25, 15 or less is ideal",
    )
    form_jp_title = models.CharField(
        "Form - Japanese Title",
        blank=False,
        null=False,
        max_length=20,
        help_text="Required. Max length 20 characters, 15 or less is ideal",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("display_title"),
            ],
            heading="Header section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("trial_en_title"),
                FieldPanel("trial_jp_title"),
                FieldPanel("trial_intro"),
                FieldPanel("trial_steps"),
            ],
            heading="Trial section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("exp_en_title"),
                FieldPanel("exp_jp_title"),
                FieldPanel("exp_intro"),
                FieldPanel("exp_steps"),
            ],
            heading="Learning experiences section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("qa_en_title"),
                FieldPanel("qa_jp_title"),
                FieldPanel("qas"),
            ],
            heading="Q and A section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("tel_en_title"),
                FieldPanel("tel_jp_title"),
                FieldPanel("tel_number"),
                FieldPanel("tel_display_number"),
            ],
            heading="Telephone contact section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("form_en_title"),
                FieldPanel("form_jp_title"),
            ],
            heading="Form contact section",
        ),
    ]

    # Api configuration
    api_fields = [
        APIField("display_title"),
        APIField("trial_en_title"),
        APIField("trial_jp_title"),
        APIField("trial_intro"),
        APIField("trial_steps"),
        APIField("exp_en_title"),
        APIField("exp_jp_title"),
        APIField("exp_intro"),
        APIField("exp_steps"),
        APIField("qa_en_title"),
        APIField("qa_jp_title"),
        APIField("qas"),
        APIField("tel_en_title"),
        APIField("tel_jp_title"),
        APIField("tel_number"),
        APIField("tel_display_number"),
        APIField("form_en_title"),
        APIField("form_jp_title"),
    ]

    max_count = 1
    parent_page_types = [
        "home.HomePage",
    ]

    def __str__(self):
        return self.title


# ======== Contact Model and associated models and logic ==========
class StatusChoices(models.IntegerChoices):
    LEAD = 0, _("Lead")
    ACTIVE_CUSTOMER = 1, _("Active Customer")
    INACTIVE_CUSTOMER = 2, _("Inactive Customer")
    BUSINESS_PARTNER = 3, _("Business Partner")
    STAFF = 4, _("Staff Member")


class IndOrOrgChoices(models.IntegerChoices):
    INDIVIDUAL = 0, _("Individual")
    ORGANIZATION = 1, _("Organization")


class GenderChoices(models.IntegerChoices):
    MALE = 0, _("Male")
    FEMALE = 1, _("Female")
    OTHER = 2, _("Other")
    NA = 3, _("Not Applicable")


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
        default="Anon",
        null=False,
        max_length=100,
        help_text="Full name in the name order and language user would like. English or 日本語 for example. Max length: 100char",
    )
    name_en = models.CharField(
        _("english name"),
        blank=True,
        null=False,
        default="Anon",
        max_length=100,
        help_text="Full name in English, order should be same as name. Example 田中たろ should become Tanaka Taro in the field. Max length: 100char",
    )
    bday = models.CharField(
        _("birthday"),
        blank=True,
        null=False,
        max_length=20,
        help_text="Birthday as day and month ex: '10 September'. Max char 20",
    )
    status = models.PositiveSmallIntegerField(
        _("Status"),
        null=False,
        blank=False,
        choices=StatusChoices.choices,
        default=StatusChoices.LEAD,
        help_text="Required",
    )
    ind_or_org = models.PositiveSmallIntegerField(
        _("Individual or Organization"),
        null=False,
        blank=False,
        choices=IndOrOrgChoices.choices,
        default=IndOrOrgChoices.INDIVIDUAL,
        help_text="Required",
    )
    gender = models.PositiveSmallIntegerField(
        _("Gender"),
        null=False,
        blank=False,
        choices=GenderChoices.choices,
        default=GenderChoices.NA,
        help_text="Required",
    )
    organization = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        limit_choices_to={"ind_or_org": 1},
        related_name="staff_members",
        null=True,
        blank=True,
        help_text="Not required",
    )
    child_of = models.ManyToManyField(
        "self",
        blank=True,
        limit_choices_to={"ind_or_org": 0},
        related_name="guardian_of",
        symmetrical=False,
        help_text="Not required",
    )
    addresses = models.ManyToManyField(
        "addresses.Address",
        through="addresses.ContactAddress",
    )

    def __str__(self) -> str:
        if self.name:  # type: ignore
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


class BannedEmail(TimeStampedModel):
    """Model to hold spam, junk and malicious emailers who mail us in the contact forms etc. Use this
    model as base for actions which prevent spam etc"""

    name = models.CharField(
        _("name"),
        null=False,
        blank=False,
        max_length=50,
        help_text="Required. Max 50. Name the emailer uses in mail. Not important, just for convenience",
    )
    email = models.EmailField(
        _("email address"),
        null=False,
        blank=False,
        max_length=150,
        unique=True,
        help_text="Required. Is unique so can only be one row for this email address. Max 150",
    )
    message = models.TextField(
        _("message"),
        null=False,
        blank=False,
        default="No mail associated",
        help_text="Required. Email sent for post mail analysis, for safety sake",
    )

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"
