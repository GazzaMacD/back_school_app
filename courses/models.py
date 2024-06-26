from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.api import APIField
from wagtail.snippets.models import register_snippet
from rest_framework.fields import Field
from wagtail_headless_preview.models import HeadlessMixin
from wagtail.fields import StreamField
from products.serializers import ClassPricePlanSerializer

from core.models import (
    TimeStampedModel,
    SubjectChoices,
    LevelChoices,
    CourseCategoryChoices,
)
from core.serializers import HeaderImageFieldSerializer
from streams import customblocks

COURSE_CHOICES_DICT = dict(CourseCategoryChoices.choices)
LEVEL_CHOICES_DICT = dict(LevelChoices.choices)


class CourseFieldSerializer(Field):
    def to_representation(self, value):
        return {
            "id": value.id,
            "title_en": value.title_en,
            "subject": value.subject,
            "subject_display": value.get_subject_display(),
            "course_category": value.course_category,
            "course_category_display": value.get_course_category_display(),
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
            "display_tagline": value.display_tagline,
            "slug": value.slug,
            "subject_slug": value.subject_slug,
            "subject_display": value.course.get_subject_display(),
            "image": {
                "id": image.id,
                "title": image.title,
                "original": image.get_rendition("original").attrs_dict,
                "medium": image.get_rendition("fill-1024x640").attrs_dict,
                "thumbnail": image.get_rendition("fill-560x350").attrs_dict,
            },
        }


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
    description = models.TextField(
        _("Description"),
        null=False,
        blank=False,
        max_length=300,
        help_text=_("A brief description of the course for internal use"),
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
    course_category = models.CharField(
        _("Course Category"),
        blank=False,
        null=False,
        max_length=20,
        default=CourseCategoryChoices.GENERAL,
        choices=CourseCategoryChoices.choices,
        help_text="Course category for the course, if in doubt make it general",
    )

    def __str__(self) -> str:
        return self.title_en


class CourseDisplayListPage(HeadlessMixin, Page):
    """Page model to for the editable content above the language courses listings"""

    display_title = models.CharField(
        "Display Title",
        blank=False,
        null=False,
        max_length=15,
        help_text="Required. Max length 15 characters. Japanese",
    )
    # Popular Courses section
    popular_en_title = models.CharField(
        "Popular - Title",
        blank=False,
        null=False,
        max_length=25,
        help_text="Required. Max length 25, 15 or less is ideal",
    )
    popular_jp_title = models.CharField(
        "Popular - Japanese Title",
        blank=False,
        null=False,
        max_length=20,
        help_text="Required. Max length 20 characters, 15 or less is ideal",
    )
    # Popular Courses section
    english_en_title = models.CharField(
        "English - Title",
        blank=False,
        null=False,
        max_length=25,
        help_text="Required. Max length 25, 15 or less is ideal",
    )
    english_jp_title = models.CharField(
        "English - Japanese Title",
        blank=False,
        null=False,
        max_length=20,
        help_text="Required. Max length 20 characters, 15 or less is ideal",
    )
    # Admin panel configuration
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("display_title"),
            ],
            heading="Courses header section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("popular_en_title"),
                FieldPanel("popular_jp_title"),
                InlinePanel("popular_courses", label="Course", max_num=4),
            ],
            heading="Popular Courses section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("english_en_title"),
                FieldPanel("english_jp_title"),
            ],
            heading="English Courses section",
        ),
    ]

    # Api configuration
    api_fields = [
        APIField("display_title"),
        APIField("popular_en_title"),
        APIField("popular_jp_title"),
        APIField("popular_courses"),
        APIField("english_en_title"),
        APIField("english_jp_title"),
    ]

    # Page limitations, Meta and methods
    max_count = 1
    parent_page_types = [
        "home.HomePage",
    ]

    # meta and other class attributes
    class Meta:
        verbose_name = "Course List Page"
        verbose_name_plural = "Courses List Pages"

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
    display_tagline = models.CharField(
        "Disply Tagline",
        blank=False,
        null=False,
        max_length=160,
        help_text="Required. Max length 160 char. A catchy, attractive tagline to give more information and sell the course",
    )
    course = models.OneToOneField(
        "courses.Course",
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        related_name="course_detail_page",
        help_text="The associated course, the page title should match exactly the name of this course",
    )
    header_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        related_name="+",
        help_text="Image size: 2048px x 1280px. Please optimize image size before uploading.",
    )
    subject_slug = models.SlugField(
        "Subect Slug",
        blank=True,
        null=False,
        help_text="Read only field that get's value from the 'course' field",
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
            ("short_text_block", customblocks.ShortCharBlock()),
        ],
        use_json_field=True,
        null=True,
        blank=False,
        min_num=6,
        max_num=10,
    )
    course_description = StreamField(
        [
            ("rich_text", customblocks.CustomRichTextBlock()),
            ("text_width_img", customblocks.StandardCustomImageBlock()),
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
                FieldPanel("display_tagline"),
                FieldPanel("course"),
                FieldPanel("header_image"),
                FieldPanel("subject_slug", read_only=True),
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
                InlinePanel("common_price_plans", label="Class Price Plan", max_num=3),
            ],
            heading="Common Associated Prices Plans",
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
        APIField("display_tagline"),
        APIField("course", serializer=CourseFieldSerializer()),
        APIField("header_image", serializer=HeaderImageFieldSerializer()),
        APIField("subject_slug"),
        APIField("level_from", serializer=LevelFieldsSerializer()),
        APIField("level_to", serializer=LevelFieldsSerializer()),
        APIField("course_content_points"),
        APIField("course_description"),
        APIField("common_price_plans"),
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


# =============== Orderables ====================


class PopularEnglishCourse(Orderable):
    """Orderable field for popular engish courses for the list page"""

    page = ParentalKey(
        CourseDisplayListPage,
        on_delete=models.CASCADE,
        related_name="popular_courses",
    )
    course = models.ForeignKey(
        "courses.CourseDisplayDetailPage", on_delete=models.CASCADE
    )

    panels = [
        FieldPanel("course"),
    ]

    api_fields = [
        APIField("course", serializer=CourseRelatedFieldSerializer()),
    ]


class RelatedCourse(Orderable):
    """Orderable field for other courses that may be connected to this course"""

    page = ParentalKey(
        CourseDisplayDetailPage,
        on_delete=models.CASCADE,
        blank=True,
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


class CommonPricePlans(Orderable):
    """Orderable field for commonly associated price plans"""

    page = ParentalKey(
        CourseDisplayDetailPage,
        on_delete=models.CASCADE,
        related_name="common_price_plans",
    )
    price_plan = models.ForeignKey(
        "products.ClassPricesDetailPage",
        on_delete=models.CASCADE,
    )

    panels = [
        FieldPanel("price_plan"),
    ]

    api_fields = [
        APIField("price_plan", serializer=ClassPricePlanSerializer()),
    ]

    def __str__(self):
        return self.price_plan.title
