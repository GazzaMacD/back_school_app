from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from modelcluster.fields import ParentalKey
from rest_framework.fields import Field
from wagtail_headless_preview.models import HeadlessMixin
from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.fields import StreamField
from wagtail.api import APIField

from core.models import Language
from streams import customblocks

# ======== Field Serializers ==========


class MemberFieldSerializer(Field):
    def to_representation(self, value):
        contact = value.contact
        return {
            "id": value.id,
            "name": contact.name,
            "name_en": contact.name_en,
        }


class LanguageSerializer(Field):
    def to_representation(self, value):
        return {
            "id": value.id,
            "name_en": value.name_en,
            "name_ja": value.name_ja,
            "slug": value.slug,
        }


class StaffProfileImageSerializer(Field):
    def to_representation(self, value):
        return {
            "id": value.id,
            "title": value.title,
            "original": value.get_rendition("original").attrs_dict,
            "thumbnail": value.get_rendition("fill-400x400").attrs_dict,
        }


# ======== Page models ==========
class StaffListPage(HeadlessMixin, Page):
    """Page to list all staff and collaborators"""

    # Fields
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

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("ja_title"),
                FieldPanel("short_intro"),
            ],
            heading="Staff List Page",
        ),
    ]

    # Api configuration
    api_fields = [
        APIField("ja_title"),
        APIField("short_intro"),
    ]

    max_count = 1
    parent_page_types = [
        "home.HomePage",
    ]

    # Methods
    def __str__(self):
        return self.title


class StaffDetailPage(HeadlessMixin, Page):
    """Page for to show detailed information about staff member or collaborator"""

    # Fields
    member = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=False,
        limit_choices_to={"is_staff": True},
        null=False,
        help_text="Required.",
    )
    profile_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        related_name="+",
        help_text="Image size: 1080px x 1080px. Please optimize image size before uploading.",
    )
    intro = models.TextField(
        "Intro",
        blank=False,
        null=False,
        max_length=200,
        help_text="Required.",
    )
    role = models.CharField(
        "Roles in company",
        blank=False,
        null=False,
        max_length=100,
        help_text="Required. Max length 100 chars",
    )
    country = models.CharField(
        "Country",
        blank=False,
        null=False,
        max_length=60,
        help_text="Required. Max length 60 chars",
    )
    native_language = models.OneToOneField(
        "core.Language",
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        help_text="Required.",
    )
    hobbies = models.CharField(
        "Hobbies",
        blank=False,
        null=False,
        max_length=255,
        help_text="Required. Comma separated list of hobbies. Max length 255 chars",
    )
    interview = StreamField(
        [
            ("youtube", customblocks.YoutubeBlock()),
            ("q_and_a", customblocks.QuestionAnswerSeriesBlock()),
        ],
        use_json_field=True,
        null=True,
        blank=False,
    )

    # Panels
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("member"),
                FieldPanel("profile_image"),
                FieldPanel("intro"),
                FieldPanel("role"),
                FieldPanel("country"),
                FieldPanel("native_language"),
                InlinePanel("languages_spoken", label="Languages Spoken"),
                FieldPanel("hobbies"),
            ],
            heading="Member details",
        ),
        MultiFieldPanel(
            [
                FieldPanel("interview"),
            ],
            heading="Interview",
        ),
    ]

    # Api
    api_fields = [
        APIField("member", serializer=MemberFieldSerializer()),
        APIField("profile_image", serializer=StaffProfileImageSerializer()),
        APIField("intro"),
        APIField("role"),
        APIField("country"),
        APIField("native_language", serializer=LanguageSerializer()),
        APIField("languages_spoken"),
        APIField("hobbies"),
        APIField("interview"),
    ]

    # Page limitations
    parent_page_types = [
        "staff.StaffListPage",
    ]

    # Methods
    def __str__(self):
        return self.title


class LanguagesSpoken(Orderable):
    """Orderable field for languages the person speaks"""

    page = ParentalKey(
        StaffDetailPage,
        on_delete=models.CASCADE,
        related_name="languages_spoken",
    )
    language = models.ForeignKey(
        "core.Language",
        on_delete=models.CASCADE,
    )

    panels = [
        FieldPanel("language"),
    ]

    api_fields = [
        APIField("language", serializer=LanguageSerializer()),
    ]

    def __str__(self):
        return self.language.name_en
