from decimal import Decimal

from django.db import models
from django.utils import timezone
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
    # prices section fields
    price_en_title = models.CharField(
        "Class Prices - English Title",
        blank=False,
        null=False,
        max_length=25,
        help_text="Required. Max length 25, 15 or less is ideal",
    )
    price_jp_title = models.CharField(
        "Class Prices - Japanese Title",
        blank=False,
        null=False,
        max_length=20,
        help_text="Required. Max length 20 characters, 15 or less is ideal",
    )
    # teacher section fields
    teacher_en_title = models.CharField(
        "Teachers - English Title",
        blank=False,
        null=False,
        max_length=25,
        help_text="Required. Max length 25, 15 or less is ideal",
    )
    teacher_jp_title = models.CharField(
        "Teachers - Japanese Title",
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
        MultiFieldPanel(
            [
                FieldPanel("price_en_title"),
                FieldPanel("price_jp_title"),
                InlinePanel(
                    "home_class_prices",
                    label="Class Prices",
                    max_num=5,
                    help_text="Choose 5 prices for this section please. Max 5.",
                ),
            ],
            heading="Class Prices",
        ),
        MultiFieldPanel(
            [
                FieldPanel("teacher_en_title"),
                FieldPanel("teacher_jp_title"),
                InlinePanel(
                    "home_teachers",
                    label="Teachers",
                    max_num=4,
                    help_text="Choose 4 teachers for this section please. Max 4.",
                ),
            ],
            heading="Teachers",
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
        APIField("price_en_title"),
        APIField("price_jp_title"),
        APIField("home_class_prices"),
        APIField("teacher_en_title"),
        APIField("teacher_jp_title"),
        APIField("home_teachers"),
    ]

    # Page limitations
    max_count = 1
    parent_page_types = ["wagtailcore.Page"]

    def __str__(self):
        return self.title


# Testimonials section for home page
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


# Prices section for home page


class HomeClassPriceSerializer(Field):
    def calculate_taxed_amount(self, price, tax_rate):
        if not isinstance(price, Decimal) or not isinstance(tax_rate, Decimal):
            return None
        return str(round(price + (price * (tax_rate / Decimal("100.00")))))

    def get_price(self, prices, tax_rate):
        filtered_prices = []
        now = int(timezone.now().timestamp())
        for price in prices:
            if now < int(price.start_date.timestamp()):
                continue
            if price.end_date and now > int(price.end_date.timestamp()):
                continue
            filtered_prices.append(price)
        filtered_prices.sort(reverse=True, key=lambda x: x.start_date)
        if len(filtered_prices) > 0:
            p = filtered_prices[0]
            return {
                "name": p.name,
                "display_name": p.display_name,
                "pretax_price": str(p.price),
                "posttax_price": self.calculate_taxed_amount(p.price, tax_rate),
                "is_sale": p.is_limited_sale,
                "start_date": p.start_date,
                "is_limited_sale": p.is_limited_sale,
                "before_sale_pretax_price": str(p.before_sale_price),
                "before_sale_posttax_price": self.calculate_taxed_amount(
                    p.before_sale_price, tax_rate
                ),
                "end_date": p.end_date,
            }
        return {}

    def to_representation(self, value):
        cs = value.class_service
        return {
            "id": value.id,
            "slug": value.slug,
            "title": value.title,
            "display_title": value.display_title,
            "length": cs.length,
            "length_unit": cs.get_length_unit_display(),
            "quantity": cs.quantity,
            "quantity_unit": cs.get_quantity_unit_display(),
            "max_num": cs.max_num,
            "is_native": cs.is_native,
            "is_online": cs.is_online,
            "is_inperson": cs.is_inperson,
            "has_onlinenotes": cs.has_onlinenotes,
            "bookable_online": cs.bookable_online,
            "price_info": self.get_price(cs.prices.all(), cs.tax_rate.rate),
        }


class HomePrices(Orderable):
    """Orderable field for class prices chosen for display on home page"""

    page = ParentalKey(
        HomePage,
        on_delete=models.CASCADE,
        related_name="home_class_prices",
    )
    class_price = models.ForeignKey(
        "products.ClassPricesDetailPage", on_delete=models.CASCADE
    )

    panels = [
        FieldPanel("class_price"),
    ]

    api_fields = [
        APIField("class_price", serializer=HomeClassPriceSerializer()),
    ]

    def __str__(self):
        return self.class_price.title


##
# Teachers Orderable and field serializer
#


class HomeTeacherSerializer(Field):
    def to_representation(self, value):
        img = value.profile_image
        return {
            "id": value.id,
            "slug": value.slug,
            "title": value.title,
            "display_name": value.display_name,
            "display_tagline": value.display_tagline,
            "image": {
                "id": img.id,
                "title": img.title,
                "original": img.get_rendition("original").attrs_dict,
                "thumbnail": img.get_rendition("fill-400x400").attrs_dict,
            },
        }


class HomeTeachers(Orderable):
    """Orderable field for chosen teachers display on home page"""

    page = ParentalKey(
        HomePage,
        on_delete=models.CASCADE,
        related_name="home_teachers",
    )
    teacher = models.ForeignKey(
        "staff.StaffDetailPage",
        on_delete=models.CASCADE,
    )

    panels = [
        FieldPanel("teacher"),
    ]

    api_fields = [
        APIField("teacher", serializer=HomeTeacherSerializer()),
    ]

    def __str__(self):
        return self.teacher.title
