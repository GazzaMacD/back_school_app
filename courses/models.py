from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.api import APIField
from wagtail.snippets.models import register_snippet
from rest_framework.fields import Field
from wagtail.fields import StreamField

from core.models import (
    TimeStampedModel,
    SubjectChoices,
    LevelChoices,
    CourseCategoryChoices,
)
from streams import customblocks

COURSE_CHOICES_DICT = dict(CourseCategoryChoices.choices)
LEVEL_CHOICES_DICT = dict(LevelChoices.choices)


class HeaderImageFieldSerializer(Field):
    def to_representation(self, value):
        return {
            "id": value.id,
            "title": value.title,
            "original": value.get_rendition("original").attrs_dict,
            "medium": value.get_rendition("fill-1280x800").attrs_dict,
            "thumbnail": value.get_rendition("fill-560x350").attrs_dict,
            "alt": value.title,
        }


class CourseFieldSerializer(Field):
    def to_representation(self, value):
        return {
            "id": value.id,
            "title_en": value.title_en,
            "subject": value.subject,
            "display": value.get_subject_display(),
        }


class CourseCategoryFieldSerializer(Field):
    def to_representation(self, value):
        return {
            "number": value,
            "display": COURSE_CHOICES_DICT[value],
        }


class LevelFieldsSerializer(Field):
    def to_representation(self, value):
        return {
            "number": value,
            "display": LEVEL_CHOICES_DICT[value],
        }


class CourseRelatedFieldSerializer(Field):
    def to_representation(self, value):
        image = value.header_image
        return {
            "id": value.id,
            "title": value.title,
            "display_title": value.display_title,
            "display_intro": value.display_intro,
            "slug": value.slug,
            "subject_slug": value.subject_slug,
            "subject_display": value.course.get_subject_display(),
            "image": {
                "id": image.id,
                "title": image.title,
                "original": image.get_rendition("original").attrs_dict,
                "thumbnail": image.get_rendition("fill-560x350").attrs_dict,
            },
        }


@register_snippet
class Course(TimeStampedModel):
    title_en = models.CharField(
        _("English Title"),
        null=False,
        blank=False,
        unique=True,
        max_length=200,
        help_text=_(
            "Subject should be included in the title. For example 'Advanced General English'. English will be the subject which also corresponds to the subject choice field"
        ),
    )
    subject = models.CharField(
        _("Subject"),
        null=False,
        blank=False,
        choices=SubjectChoices.choices,
        max_length=20,
        default=SubjectChoices.ENGLISH,
        help_text="Required",
    )

    def __str__(self) -> str:
        return self.title_en


class CourseDisplayListPage(Page):
    """Page model to for the editable content above the course listings"""

    display_title = models.CharField(
        "Display Title",
        blank=False,
        null=False,
        max_length=100,
        help_text="Required. Max length 100 characters, 45 or less is ideal",
    )
    # Admin panel configuration
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("display_title"),
            ],
            heading="Course header section",
        ),
    ]

    # Api configuration
    api_fields = [
        APIField("display_title"),
    ]

    # Page limitations, Meta and methods
    max_count = 1
    parent_page_types = [
        "home.HomePage",
    ]

    # meta and other class attributes
    class Meta:
        verbose_name = "Course Display List Page"
        verbose_name_plural = "Course Display List Pages"

    def __str__(self):
        return self.title


class CourseDisplayDetailPage(Page):
    """Page model to show details about course on the site for marketing purposes"""

    display_title = models.CharField(
        "Display Title",
        blank=False,
        null=False,
        max_length=100,
        help_text="Required. Max length 100 characters, 45 or less is ideal",
    )
    course = models.OneToOneField(
        "courses.Course",
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        related_name="course_detail_page",
        help_text="The associated course",
    )
    header_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        related_name="+",
        help_text="Image size: 2048px x 1280px. Please optimize image size before uploading.",
    )
    display_intro = models.TextField(
        "Display Introduction",
        blank=False,
        null=False,
        max_length=150,
        help_text="Required. Max length 150.",
    )
    subject_slug = models.SlugField(
        "Subect Slug",
        blank=True,
        null=False,
        help_text="Read only field that get's value from the 'course' field",
    )
    course_category = models.PositiveSmallIntegerField(
        _("Course Category"),
        blank=False,
        null=False,
        default=CourseCategoryChoices.GENERAL,
        choices=CourseCategoryChoices.choices,
        help_text="Course category for the course, if in doubt make it general",
    )
    level_from = models.PositiveSmallIntegerField(
        _("Level From"),
        blank=False,
        null=False,
        choices=LevelChoices.choices,
        help_text="Starting level. If no 'to level' or this is 'all' levels then please enter 'to level' as None.",
    )
    level_to = models.PositiveSmallIntegerField(
        _("Level To"),
        blank=False,
        null=False,
        default=LevelChoices.NONE,
        choices=LevelChoices.choices,
        help_text="Starting level. If no 'to level' then please mark 'to level' as None.",
    )
    # Page content section fields
    course_content_points = StreamField(
        [
            ("listblock", customblocks.ListBlock()),
        ],
        use_json_field=True,
        null=True,
        blank=False,
    )
    course_description = StreamField(
        [
            ("rich_text", customblocks.CustomRichTextBlock()),
            ("text_width_img", customblocks.ContentWidthImage()),
            ("youtube", customblocks.YoutubeBlock()),
        ],
        use_json_field=True,
        null=True,
        blank=False,
    )

    # Admin panel configuration
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("display_title"),
                FieldPanel("course"),
                FieldPanel("header_image"),
                FieldPanel("subject_slug", read_only=True),
                FieldPanel("display_intro"),
                FieldPanel("course_category"),
                FieldPanel("level_from"),
                FieldPanel("level_to"),
            ],
            heading="Course header section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("course_content_points"),
            ],
            heading="Course Content Points",
        ),
        MultiFieldPanel(
            [
                FieldPanel("course_description"),
            ],
            heading="Course Description",
        ),
        MultiFieldPanel(
            [
                InlinePanel("related_courses", label="Course", max_num=4),
            ],
            heading="Related Courses",
        ),
    ]

    # Api configuration
    api_fields = [
        APIField("display_title"),
        APIField("course", serializer=CourseFieldSerializer()),
        APIField("header_image", serializer=HeaderImageFieldSerializer()),
        APIField("subject_slug"),
        APIField("display_intro"),
        APIField("course_category", serializer=CourseCategoryFieldSerializer()),
        APIField("level_from", serializer=LevelFieldsSerializer()),
        APIField("level_to", serializer=LevelFieldsSerializer()),
        APIField("course_content_points"),
        APIField("course_description"),
        APIField("related_courses"),
    ]

    # Page limitations, Meta and methods
    parent_page_types = [
        "courses.CourseDisplayListPage",
    ]

    # meta and other class attributes
    class Meta:
        verbose_name = "Course Display Detail Page"
        verbose_name_plural = "Course Display Detail Pages"

    def __str__(self):
        return self.title

    def full_clean(self, *args, **kwargs):
        """Use full clean to manipulate subject_slug, title and slug so as to be consistent
        with the base course django model"""
        super().full_clean(*args, **kwargs)
        if not self.subject_slug == self.course.subject:
            self.subject_slug = self.course.subject

        if not self.title == self.course.title_en:
            self.title = self.course.title_en

        if not self.slug == slugify(self.course.title_en):
            self.slug = slugify(self.course.title_en)


# Override Detail Page title helptextoo
CourseDisplayDetailPage._meta.get_field(
    "title"
).help_text = "The title should match the linked 'course' field title. If it doesn't it will be replaced."


class RelatedCourse(Orderable):
    """Orderable field for other courses that may be connected to this course"""

    page = ParentalKey(
        CourseDisplayDetailPage,
        on_delete=models.CASCADE,
        related_name="related_courses",
    )
    course = models.ForeignKey(
        "courses.CourseDisplayDetailPage",
        on_delete=models.CASCADE,
    )

    panels = [
        FieldPanel("course"),
    ]

    api_fields = [
        APIField("course", serializer=CourseRelatedFieldSerializer()),
    ]

    def __str__(self):
        return self.course.title
