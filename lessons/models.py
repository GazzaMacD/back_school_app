from django.db import models
from django.utils import timezone
from rest_framework.fields import Field
from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.snippets.models import register_snippet
from wagtail_headless_preview.models import HeadlessMixin
from wagtail.api import APIField
from wagtail.fields import StreamField

from streams import customblocks
from core.serializers import HeaderImageFieldSerializer


# Field Serializers
class LessonAuthorFieldSerializer(Field):
    def to_representation(self, value):
        profile_image = value.profile_image
        return {
            "id": value.id,
            "title": value.title,
            "slug": value.slug,
            "name": value.member.contact.name,
            "image": {
                "id": profile_image.id,
                "title": profile_image.title,
                "original": profile_image.get_rendition("original").attrs_dict,
                "thumbnail": profile_image.get_rendition("fill-400x400").attrs_dict,
            },
        }


class LessonCategoryFieldSerializer(Field):
    def to_representation(self, value):
        return {
            "id": value.id,
            "name": value.name,
            "ja_name": value.ja_name,
            "slug": value.slug,
        }


# Pages
class LessonListPage(HeadlessMixin, Page):
    """Page where blog lessons will be categorized and listed"""

    # Model fields
    display_title = models.CharField(
        "Display Title",
        blank=False,
        null=False,
        max_length=100,
        help_text="Required. Max length 15 characters.",
    )
    # Admin panel configuration
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("display_title"),
            ],
            heading="Header area",
        )
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

    class Meta:
        verbose_name = "Blog Lessons List Page"
        verbose_name_plural = "Blog Lessons List Pages"

    def __str__(self):
        return self.title

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.title!r})"


class LessonDetailPage(HeadlessMixin, Page):
    """Blog Lesson Detail page with variable content options provided by stream fields"""

    # Page header fields
    header_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        related_name="+",
        help_text="Image size: 2048px x 1280px. Please optimize image size before uploading.",
    )
    author = models.ForeignKey(
        "staff.StaffDetailPage",
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        related_name="lessons",
        help_text="Author of this lesson",
    )
    display_title = models.CharField(
        "Display Title",
        blank=False,
        null=False,
        max_length=100,
        help_text="Required. Max length 100 characters, 45 or less is ideal",
    )
    display_tagline = models.CharField(
        "Display Tagline",
        blank=False,
        null=False,
        max_length=200,
        help_text="A catchy, short introduction of what the blog lesson is about. Max length 200 chars",
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
        help_text="Estimated time in minutes to complete this lesson",
    )
    category = models.ForeignKey(
        "lessons.LessonCategory",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Please categorize the lesson",
    )
    # Page main content fields
    lesson_content = StreamField(
        [
            ("rich_text", customblocks.CustomRichTextBlock()),
            ("block_quote", customblocks.BlockQuoteBlock()),
            ("full_width_img", customblocks.StandardCustomImageBlock()),
            ("beyond_text_img", customblocks.StandardCustomImageBlock()),
            ("text_width_img", customblocks.StandardCustomImageBlock()),
            ("youtube", customblocks.YoutubeBlock()),
            ("conversation", customblocks.ConversationBlock()),
            ("wrong_right_list", customblocks.WrongRightListBlock()),
            ("examples_list", customblocks.ExamplesListBlock()),
            ("mc_questions", customblocks.MCQuestionsBlock()),
        ],
        use_json_field=True,
        null=True,
        blank=False,
    )

    # Admin panel configuration
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("header_image"),
                FieldPanel("author"),
                FieldPanel("display_title"),
                FieldPanel("display_tagline"),
                FieldPanel("published_date"),
                FieldPanel("estimated_time"),
                FieldPanel("category"),
            ],
            heading="Lesson detail page header area",
        ),
        FieldPanel("lesson_content"),
        MultiFieldPanel(
            [
                InlinePanel(
                    "related_simple_banner_campaigns",
                    label="Simple Banner Campaign",
                    max_num=2,
                ),
            ],
            heading="Campaigns",
        ),
        MultiFieldPanel(
            [
                InlinePanel("related_lessons", label="Lesson", max_num=4),
            ],
            heading="Related Lessons",
        ),
    ]

    # Api configuration
    api_fields = [
        APIField("header_image", serializer=HeaderImageFieldSerializer()),
        APIField("author", serializer=LessonAuthorFieldSerializer()),
        APIField("display_title"),
        APIField("display_tagline"),
        APIField("published_date"),
        APIField("estimated_time"),
        APIField("category", serializer=LessonCategoryFieldSerializer()),
        APIField("lesson_content"),
        APIField("related_simple_banner_campaigns"),
        APIField("related_lessons"),
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


@register_snippet
class LessonCategory(models.Model):
    name = models.CharField(
        "Category name",
        blank=False,
        unique=True,
        null=False,
        max_length=30,
        help_text="English name for category, max 30 chars.",
    )
    ja_name = models.CharField(
        "Japanese Category name",
        blank=False,
        unique=True,
        null=False,
        max_length=30,
        help_text="English name for category, max 30 chars.",
    )
    slug = models.SlugField(
        unique=True,
        blank=False,
        null=False,
        max_length=40,
        help_text="Use English name to create a slug with only hypens and lowercase letters",
    )
    panels = [
        FieldPanel("name"),
        FieldPanel("ja_name"),
        FieldPanel("slug"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Lesson Category"
        verbose_name_plural = "Lesson Categories"


# =======
# Related Lessons
# =======


class LessonRelatedFieldSerializer(Field):
    def to_representation(self, value):
        image = value.header_image
        return {
            "id": value.id,
            "title": value.title,
            "display_title": value.display_title,
            "published_date": value.published_date,
            "display_tagline": value.display_tagline,
            "slug": value.slug,
            "category": {
                "name": value.category.name,
                "ja_name": value.category.ja_name,
                "slug": value.category.slug,
            },
            "image": {
                "id": image.id,
                "title": image.title,
                "original": image.get_rendition("original").attrs_dict,
                "thumbnail": image.get_rendition("fill-560x350").attrs_dict,
            },
        }


class RelatedLessons(Orderable):
    """Orderable field for lessons that should be connected to this lesson"""

    page = ParentalKey(
        LessonDetailPage,
        on_delete=models.CASCADE,
        related_name="related_lessons",
    )
    lesson = models.ForeignKey(
        "lessons.LessonDetailPage",
        on_delete=models.CASCADE,
    )

    panels = [
        FieldPanel("lesson"),
    ]

    api_fields = [
        APIField("lesson", serializer=LessonRelatedFieldSerializer()),
    ]

    def __str__(self):
        return self.lesson.title


# =======
# Related Campaigns
# =======


class RelatedSimpleBannerCampaignFieldSerializer(Field):
    def to_representation(self, value):
        return {
            "id": value.id,
            "title": value.title,
            "slug": value.slug,
            "campaign_page_type": value.campaign_page_type,
            "color_type": value.color_type,
            "name_ja": value.name_ja,
            "offer": value.offer,
            "start_date": value.start_date,
            "end_date": value.end_date,
        }


class RelatedSimpleBannerCampaign(Orderable):
    page = ParentalKey(
        LessonDetailPage,
        on_delete=models.CASCADE,
        related_name="related_simple_banner_campaigns",
    )
    campaign = models.ForeignKey(
        "campaigns.CampaignSimpleBannerPage",
        on_delete=models.CASCADE,
    )
    panels = [
        FieldPanel("campaign"),
    ]
    api_fields = [
        APIField("campaign", serializer=RelatedSimpleBannerCampaignFieldSerializer()),
    ]

    def __str__(self):
        return self.campaign.title
