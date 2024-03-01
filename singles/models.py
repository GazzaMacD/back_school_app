from django.db import models
from wagtail_headless_preview.models import HeadlessMixin
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.api import APIField


class PrivacyPage(HeadlessMixin, Page):
    # Model fields
    display_title = models.CharField(
        "Display Title",
        blank=False,
        null=False,
        max_length=15,
        help_text="Required. Max length 15 characters. Japanese",
    )
    content = RichTextField(
        features=[
            "h2",
            "h3",
            "h4",
            "ul",
            "ol",
            "link",
            "bold",
        ],
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
                FieldPanel("content"),
            ],
            heading="Main Section",
        ),
    ]

    # API Section
    api_fields = [
        APIField("display_title"),
        APIField("content"),
    ]

    # Limitations and functions
    max_count = 1
    parent_page_types = [
        "home.HomePage",
    ]

    def __str__(self):
        return self.title
