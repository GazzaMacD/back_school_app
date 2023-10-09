from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import StreamField
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.api import APIField
from wagtail_headless_preview.models import HeadlessMixin
from rest_framework.fields import Field

from streams import customblocks


class StaffMembersFieldSerializer(Field):
    def to_representation(self, value):
        image = value.profile_image
        return {
            "id": value.id,
            "name": value.title,
            "slug": value.slug,
            "position": value.role,
            "intro": value.intro,
            "image": {
                "id": image.id,
                "title": image.title,
                "original": image.get_rendition("original").attrs_dict,
                "thumbnail": image.get_rendition("fill-450x450").attrs_dict,
            },
        }


class AboutPage(HeadlessMixin, Page):
    """A page to deliver mixed content for /about on site"""

    # Model fields
    display_title = models.CharField(
        "Display Title",
        blank=False,
        null=False,
        max_length=15,
        help_text="Required. Max length 15 characters. English",
    )
    # Mission section
    mission_title = models.CharField(
        "Mission Title",
        blank=False,
        null=False,
        max_length=15,
        help_text="Required. Max length 15 characters.",
    )
    mission_tagline = models.CharField(
        "Mission Tagline",
        blank=False,
        null=False,
        max_length=100,
        help_text="Required. Max length 100 characters. Japanese",
    )
    mission_content = models.TextField(
        "Mission Content",
        blank=False,
        null=False,
        max_length=300,
        help_text="Required. Max length 300 characters.",
    )

    # Staff section
    staff_title = models.CharField(
        "Staff Title",
        blank=False,
        null=False,
        max_length=15,
        help_text="Required. Max length 15 characters.",
    )
    staff_tagline = models.CharField(
        "Staff Tagline",
        blank=False,
        null=False,
        max_length=100,
        help_text="Required. Max length 100 characters. Japanese",
    )

    # Core values section
    values_title = models.CharField(
        "Core Values Title",
        blank=False,
        null=False,
        max_length=15,
        help_text="Required. Max length 15 characters.",
    )
    values_tagline = models.CharField(
        "Core Values Tagline",
        blank=False,
        null=False,
        max_length=100,
        help_text="Required. Max length 100 characters. Japanese",
    )
    values_content = StreamField(
        [
            ("rich_text", customblocks.CustomRichTextBlock()),
            ("value_cards", customblocks.InfoCardSeriesBlock()),
        ],
        use_json_field=True,
        null=True,
        blank=False,
    )

    # History section
    history_title = models.CharField(
        "History Title",
        blank=False,
        null=False,
        max_length=15,
        help_text="Required. Max length 15 characters.",
    )
    history_tagline = models.CharField(
        "History Tagline",
        blank=False,
        null=False,
        max_length=100,
        help_text="Required. Max length 100 characters. Japanese",
    )
    history_content = StreamField(
        [
            ("rich_text", customblocks.CustomRichTextBlock()),
        ],
        use_json_field=True,
        null=True,
        blank=False,
    )

    # Panels
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("display_title"),
            ],
            heading="Header",
        ),
        MultiFieldPanel(
            [
                FieldPanel("mission_title"),
                FieldPanel("mission_tagline"),
                FieldPanel("mission_content"),
            ],
            heading="Mission Section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("staff_title"),
                FieldPanel("staff_tagline"),
                InlinePanel("staff_members", label="Staff Member"),
            ],
            heading="Staff Section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("values_title"),
                FieldPanel("values_tagline"),
                FieldPanel("values_content"),
            ],
            heading="Core Values Section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("history_title"),
                FieldPanel("history_tagline"),
                FieldPanel("history_content"),
            ],
            heading="History Section",
        ),
    ]

    # API Section
    api_fields = [
        APIField("display_title"),
        APIField("mission_title"),
        APIField("mission_tagline"),
        APIField("mission_content"),
        APIField("staff_title"),
        APIField("staff_tagline"),
        APIField("staff_members"),
        APIField("values_title"),
        APIField("values_tagline"),
        APIField("values_content"),
        APIField("history_title"),
        APIField("history_tagline"),
        APIField("history_content"),
    ]

    # Limitations and functions
    max_count = 1
    parent_page_types = [
        "home.HomePage",
    ]

    def __str__(self):
        return self.title


class AboutPageStaff(Orderable):
    page = ParentalKey(
        AboutPage,
        on_delete=models.CASCADE,
        related_name="staff_members",
    )
    staff = models.ForeignKey(
        "staff.StaffDetailPage",
        on_delete=models.CASCADE,
    )
    # Panels

    panels = [FieldPanel("staff")]

    api_fields = [
        APIField("staff", serializer=StaffMembersFieldSerializer()),
    ]

    def __str__(self):
        return self.staff.title