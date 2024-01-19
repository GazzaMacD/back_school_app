from django.db import models

from rest_framework.fields import Field
from wagtail_headless_preview.models import HeadlessMixin
from wagtail.models import Page, Orderable
from modelcluster.fields import ParentalKey
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
    why_content = RichTextField(
        features=["bold"],
    )
    # service section fields
    service_en_title = models.CharField(
        "Services - English Title",
        blank=False,
        null=False,
        max_length=25,
        help_text="Required. Max length 25, 15 or less is ideal",
    )
    service_jp_title = models.CharField(
        "Services - Japanese Title",
        blank=False,
        null=False,
        max_length=20,
        help_text="Required. Max length 20 characters, 15 or less is ideal",
    )
    service_cards = StreamField(
        [
            ("square_pic_cards", customblocks.SquarePicCardBlock(label="Service Card")),
        ],
        block_counts={
            "square_pic_cards": {"max_num": 4},
        },
        use_json_field=True,
        blank=True,
    )
    # testimonial section fields
    testimonial_en_title = models.CharField(
        "Testimonials - English Title",
        blank=False,
        null=False,
        max_length=25,
        help_text="Required. Max length 25, 15 or less is ideal",
    )
    testimonial_jp_title = models.CharField(
        "Testimonials - Japanese Title",
        blank=False,
        null=False,
        max_length=20,
        help_text="Required. Max length 20 characters, 15 or less is ideal",
    )

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
        MultiFieldPanel(
            [
                FieldPanel("service_en_title"),
                FieldPanel("service_jp_title"),
                FieldPanel("service_cards"),
            ],
            heading="Our services",
        ),
        MultiFieldPanel(
            [
                FieldPanel("testimonial_en_title"),
                FieldPanel("testimonial_jp_title"),
                InlinePanel(
                    "home_testimonials",
                    label="Testimonial",
                    max_num=2,
                    help_text="Choose 2 testimonials for this section please. Max 2.",
                ),
            ],
            heading="Testimonials",
        ),
    ]

    # Api configuration
    api_fields = [
        APIField("why_en_title"),
        APIField("why_jp_title"),
        APIField("why_image", serializer=HeaderImageFieldSerializer()),
        APIField("why_content"),
        APIField("service_en_title"),
        APIField("service_jp_title"),
        APIField("service_cards"),
        APIField("testimonial_en_title"),
        APIField("testimonial_jp_title"),
        APIField("home_testimonials"),
    ]

    # Page limitations
    max_count = 1
    parent_page_types = ["wagtailcore.Page"]

    def __str__(self):
        return self.title


class HomeTestimonialSerializer(Field):
    def to_representation(self, value):
        img = value.customer_portrait_image
        return {
            "id": value.id,
            "slug": value.slug,
            "title": value.title,
            "customer_name": value.customer_name,
            "occupation": value.occupation,
            "lead_sentence": value.lead_sentence,
            "comment": value.comment,
            "image": {
                "id": img.id,
                "title": img.title,
                "medium": img.get_rendition("fill-1400x1800").attrs_dict,
            },
        }


class HomeTestimonials(Orderable):
    """Orderable field for testimonials chosen for display on home page"""

    page = ParentalKey(
        HomePage,
        on_delete=models.CASCADE,
        related_name="home_testimonials",
    )
    testimonial = models.ForeignKey(
        "testimonials.TestimonialDetailPage", on_delete=models.CASCADE
    )

    panels = [
        FieldPanel("testimonial"),
    ]

    api_fields = [
        APIField("testimonial", serializer=HomeTestimonialSerializer()),
    ]

    def __str__(self):
        return self.testimonial.title
