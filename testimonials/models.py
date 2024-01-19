from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from rest_framework.fields import Field
from wagtail_headless_preview.models import HeadlessMixin
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField, RichTextField
from wagtail.api import APIField

from streams import customblocks
from django.db import models


class CustomerSquareImageSerializer(Field):
    def to_representation(self, value):
        return {
            "id": value.id,
            "title": value.title,
            "original": value.get_rendition("original").attrs_dict,
            "medium": value.get_rendition("fill-740x740").attrs_dict,
            "thumbnail": value.get_rendition("fill-400x400").attrs_dict,
        }


class CustomerPortraitImageSerializer(Field):
    def to_representation(self, value):
        return {
            "id": value.id,
            "title": value.title,
            "original": value.get_rendition("original").attrs_dict,
            "medium": value.get_rendition("fill-1400x1800").attrs_dict,
            "thumbnail": value.get_rendition("fill-560x720").attrs_dict,
        }


class TestimonialListPage(HeadlessMixin, Page):
    """Testimonial Page all testimonials and google reviews will be on this page"""

    # Model fields
    display_title = models.CharField(
        "Display Title",
        blank=False,
        null=False,
        max_length=15,
        help_text="Required. Max length 30 characters.",
    )
    tagline = models.CharField(
        "Tagline",
        blank=False,
        null=False,
        max_length=90,
        help_text="Required. Max length 90 characters.",
    )

    # Admin panel configuration
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("display_title"),
                FieldPanel("tagline"),
            ],
            heading="Testimonial List Page Header Section ",
        )
    ]

    # Api configuration
    api_fields = [
        APIField("display_title"),
        APIField("tagline"),
    ]

    # Page limitations, Meta and methods
    max_count = 1
    parent_page_types = [
        "home.HomePage",
    ]

    class Meta:
        verbose_name = "Testimonial list page"

    def __str__(self):
        return self.title


class TestimonialDetailPage(HeadlessMixin, Page):
    """A model for displaying customer reviews and interviews on the site"""

    customer_name = models.CharField(
        "Customer name",
        blank=False,
        null=False,
        max_length=100,
        help_text="Required. Max length 100 chars",
    )
    customer_square_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        related_name="+",
        help_text="Image size: 1080px x 1080px (1:1). Please optimize image size before uploading.",
    )
    customer_portrait_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        related_name="+",
        help_text="Image size: 1400 x 1800px (7:9). Please optimize image size before uploading.",
    )
    occupation = models.CharField(
        "Occupation of customer",
        blank=True,
        null=False,
        max_length=100,
        help_text="Not required. Max length 100 chars",
    )
    organization_name = models.CharField(
        "Organization affiliated with",
        blank=True,
        null=False,
        max_length=100,
        help_text="Not required but adds to veracity of testimonial. Max length 100 chars.",
    )
    organization_url = models.URLField(
        "Url for organization",
        blank=True,
        null=False,
        max_length=100,
        help_text="Not required but adds to veracity of testimonial. Max length 100 chars.",
    )
    published_date = models.DateTimeField(
        blank=False,
        null=False,
        default=timezone.now,
        help_text="IMPORTANT NOTE: This date will affect the order on list pages.",
    )
    lead_sentence = models.CharField(
        "Lead Sentence",
        blank=True,
        null=False,
        max_length=30,
        help_text="Required. 30char max. One small sentence to describe their feeling about the company",
    )
    comment = RichTextField(
        "Short Comment",
        blank=False,
        null=False,
        max_length=300,
        features=["bold"],
        help_text="Required. Max length 300 chars. A short comment about the company to display in places on site.",
    )
    customer_interview = StreamField(
        [
            ("youtube", customblocks.YoutubeBlock()),
            ("conversation", customblocks.ConversationBlock()),
        ],
        use_json_field=True,
        null=True,
        blank=False,
    )

    # Admin panel configuration
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("customer_name"),
                FieldPanel("customer_square_image"),
                FieldPanel("customer_portrait_image"),
                FieldPanel("occupation"),
                FieldPanel("organization_name"),
                FieldPanel("organization_url"),
                FieldPanel("published_date"),
            ],
            heading="Testimonial header",
        ),
        MultiFieldPanel(
            [
                FieldPanel("lead_sentence"),
                FieldPanel("comment"),
                FieldPanel("customer_interview"),
            ],
            heading="Testimonial Comment and Interview",
        ),
    ]

    # Api configuration
    api_fields = [
        APIField("customer_name"),
        APIField("customer_square_image", serializer=CustomerSquareImageSerializer()),
        APIField(
            "customer_portrait_image", serializer=CustomerPortraitImageSerializer()
        ),
        APIField("occupation"),
        APIField("organization_name"),
        APIField("organization_url"),
        APIField("published_date"),
        APIField("comment"),
        APIField("customer_interview"),
    ]

    # Page limitations, Meta and methods
    parent_page_types = [
        "testimonials.TestimonialListPage",
    ]

    # meta and other class attributes
    class Meta:
        verbose_name = "Testimonial Detail Page"
        verbose_name_plural = "Testimonial Detail Pages"
        ordering = ["-published_date"]

    def __str__(self):
        return self.title
