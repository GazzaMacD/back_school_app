from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import StreamField
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.api import APIField
from wagtail_headless_preview.models import HeadlessMixin
from wagtail.fields import RichTextField
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
            "display_tagline": value.display_tagline,
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
        help_text="Required. Max length 15 characters. Japanese",
    )
    # Mission section
    mission_en_title = models.CharField(
        "Mission Title",
        blank=False,
        null=False,
        max_length=25,
        help_text="Required. Max length 25, 15 or less is ideal",
    )
    mission_jp_title = models.CharField(
        "Mission - Japanese Title",
        blank=False,
        null=False,
        max_length=20,
        help_text="Required. Max length 20 characters, 15 or less is ideal",
    )
    mission_content = models.TextField(
        "Mission Content",
        blank=False,
        null=False,
        max_length=300,
        help_text="Required. Max length 300 characters.",
    )

    # Staff section
    staff_en_title = models.CharField(
        "Staff - English Title",
        blank=False,
        null=False,
        max_length=25,
        help_text="Required. Max length 25, 15 or less is ideal",
    )
    staff_jp_title = models.CharField(
        "Staff - Japanese Title",
        blank=False,
        null=False,
        max_length=20,
        help_text="Required. Max length 20 characters, 15 or less is ideal",
    )

    # Core values section
    values_en_title = models.CharField(
        "Values - English Title",
        blank=False,
        null=False,
        max_length=25,
        help_text="Required. Max length 25, 15 or less is ideal",
    )
    values_jp_title = models.CharField(
        "Values - Japanese Title",
        blank=False,
        null=False,
        max_length=20,
        help_text="Required. Max length 20 characters, 15 or less is ideal",
    )
    values_intro = RichTextField(
        features=["bold"],
    )
    values_list = StreamField(
        [
            ("value_cards", customblocks.InfoCardBlockBilingual()),
        ],
        use_json_field=True,
        null=True,
        blank=False,
        max_num=6,
    )

    # History section
    history_en_title = models.CharField(
        "History - English Title",
        blank=False,
        null=False,
        max_length=25,
        help_text="Required. Max length 25, 15 or less is ideal",
    )
    history_jp_title = models.CharField(
        "History - Japanese Title",
        blank=False,
        null=False,
        max_length=20,
        help_text="Required. Max length 20 characters, 15 or less is ideal",
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
                FieldPanel("mission_en_title"),
                FieldPanel("mission_jp_title"),
                FieldPanel("mission_content"),
            ],
            heading="Mission Section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("staff_en_title"),
                FieldPanel("staff_jp_title"),
                InlinePanel("staff_members", label="Staff Member"),
            ],
            heading="Staff Section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("values_en_title"),
                FieldPanel("values_jp_title"),
                FieldPanel("values_intro"),
                FieldPanel("values_list"),
            ],
            heading="Core Values Section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("history_en_title"),
                FieldPanel("history_jp_title"),
                FieldPanel("history_content"),
            ],
            heading="History Section",
        ),
    ]

    # API Section
    api_fields = [
        APIField("display_title"),
        APIField("mission_en_title"),
        APIField("mission_jp_title"),
        APIField("mission_content"),
        APIField("staff_en_title"),
        APIField("staff_jp_title"),
        APIField("staff_members"),
        APIField("values_en_title"),
        APIField("values_jp_title"),
        APIField("values_intro"),
        APIField("values_list"),
        APIField("history_en_title"),
        APIField("history_jp_title"),
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
