from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from django.utils import timezone

from wagtail_headless_preview.models import HeadlessMixin
from wagtail.api import APIField


class LessonListPage(HeadlessMixin, Page):
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


class LessonDetailPage(HeadlessMixin, Page):
    """Lesson Detail page with variable content options provided by stream fields"""

    # Page header fields
    header_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        related_name="+",
        help_text="Image size: 2048px x 1280px",
    )
    jp_title = models.CharField(
        "Japanese Title",
        blank=False,
        null=False,
        max_length=70,
        help_text="Required. Max length 70 characters, 60 or less is ideal",
    )
    published_date = models.DateTimeField(
        blank=False,
        null=False,
        default=timezone.now,
        help_text="IMPORTANT NOTE: This date will affect the order on list pages.",
    )
    estimated_time = models.PositiveSmallIntegerField(
        blank=False,
        null=False,
        help_text="Estimated time to complete this lesson",
    )
    # Page header fields

    # Admin panel configuration
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("header_image"),
                FieldPanel("jp_title"),
                FieldPanel("published_date"),
                FieldPanel("estimated_time"),
            ],
            heading="Lesson detail page header area",
        )
    ]

    # Api configuration
    api_fields = [
        APIField("header_image"),
        APIField("jp_title"),
        APIField("published_date"),
        APIField("estimated_time"),
    ]

    # Page limitations, Meta and methods
    parent_page_types = [
        "lessons.LessonListPage",
    ]

    # meta and other class attributes
    class Meta:
        verbose_name = "Lesson Detail Page"
        verbose_name_plural = "Lesson Detail Pages"
        ordering = ["-published_date"]

    def __str__(self):
        return self.title

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.title!r})"
