from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.api import APIField


class LessonListPage(Page):
    """Page where lessons will be categorized and listed"""

    # Model fields
    jp_title = models.CharField(
        "Japanese Title",
        blank=False,
        null=False,
        max_length=70,
        help_text="Required. Max length 70 characters, 60 or less is ideal",
    )
    # Admin panel configuration
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("jp_title"),
            ],
            heading="Lesson list page header area",
        )
    ]

    # Api configuration
    api_fields = [
        APIField("jp_title"),
    ]

    # Page limitations, Meta and methods
    max_count = 1
    parent_page_types = [
        "home.HomePage",
    ]

    class Meta:
        verbose_name = "Lesson list page"

    def __str__(self):
        return self.title

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.title!r})"
