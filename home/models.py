from django.db import models

from wagtail_headless_preview.models import HeadlessMixin
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.api import APIField
from wagtail.fields import StreamField

from streams import customblocks
from core.serializers import HeaderImageFieldSerializer


class HomePage(HeadlessMixin, Page):
    why_en_title = models.CharField(
        "Why - English Title",
        blank=False,
        null=False,
        max_length=25,
        help_text="Required. Max length 25 characters, 20 or less is ideal",
    )
    why_jp_title = models.CharField(
        "Why - Japanese Title",
        blank=False,
        null=False,
        max_length=20,
        help_text="Required. Max length 20 characters, 15 or less is ideal",
    )
    why_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        related_name="+",
        help_text="Image size: 2048px x 1280px. Please optimize image size before uploading.",
    )
    why_content = RichTextField(features=["bold"])

    # Admin panel configuration
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("why_en_title"),
                FieldPanel("why_jp_title"),
                FieldPanel("why_image"),
                FieldPanel("why_content"),
            ],
            heading="Why learn with us",
        ),
    ]

    # Api configuration
    api_fields = [
        APIField("why_en_title"),
        APIField("why_jp_title"),
        APIField("why_image", serializer=HeaderImageFieldSerializer()),
        APIField("why_content"),
    ]

    # Page limitations
    max_count = 1
    parent_page_types = ["wagtailcore.Page"]

    def __str__(self):
        return self.title
