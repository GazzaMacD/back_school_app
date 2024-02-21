from decimal import Decimal

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from modelcluster.fields import ParentalKey
from rest_framework.fields import Field
from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.fields import RichTextField, StreamField
from wagtail.api import APIField
from wagtail_headless_preview.models import HeadlessMixin

from streams import customblocks
from core.models import TimeStampedModel
from core.serializers import HeaderImageFieldSerializer
from lessons.models import LessonRelatedFieldSerializer

# =====================
# Model Choices
# =====================


class ProductServiceTypeChoices(models.TextChoices):
    CLASS = "class", "Class"
    EXPERIENCE = "experience", "Learning Experience"
    BOOK = "book", "Book"
    JOINIING_FEE = "joiningfee", "Joining Fee"


class ProductOrServiceChoices(models.TextChoices):
    SERVICE = "service", "Service"
    PRODUCT = "product", "Product"


class ClassTypeChoices(models.TextChoices):
    NA = "na", "N/a"
    PRIVATE = "private", "Private,プライベート"
    REGULAR = "regular", "Regular,一般"


class GroupOrOneChoices(models.TextChoices):
    NA = "na", "N/a"
    O2O = "one-to-one", "OneToOne,マンツーマン"
    GROUP = "group", "Group,グループ"


class LengthUnitChoices(models.TextChoices):
    NA = "na", "N/a"
    MINUTES = "minutes", "Minutes,分"
    WORDS = "words", "Words,単語"


class QuantityUnitChoices(models.TextChoices):
    NA = "na", "N/a"
    WEEK = "week", "Week,週"
    MONTH = "month", "Month,月"
    YEAR = "year", "Year,年"
    PAYMENT = "payment", "Payment,支払"


# =====================
# Models
# =====================


class ProductService(TimeStampedModel):
    """Model for all products and services sold by the company"""

    name = models.CharField(
        _("Name"),
        blank=False,
        null=False,
        max_length=200,
        help_text=_("Required. Max length 200 characters. English."),
    )
    slug = models.SlugField(
        _("Slug"),
        null=False,
        blank=False,
        unique=True,
        editable=False,
        max_length=100,
        help_text=_(
            "Autogenerated slug. Base slug for product model and any product display models"
        ),
    )
    service_or_product = models.CharField(
        _("Service or Product"),
        null=False,
        blank=False,
        max_length=20,
        choices=ProductOrServiceChoices.choices,
        help_text="Required",
    )
    ptype = models.CharField(
        _("Product or Service Type"),
        null=False,
        blank=False,
        max_length=20,
        choices=ProductServiceTypeChoices.choices,
        help_text="Required",
    )
    group_or_one = models.CharField(
        _("Group or 1-to-1"),
        null=False,
        blank=False,
        max_length=20,
        default=GroupOrOneChoices.NA,
        choices=GroupOrOneChoices.choices,
        help_text="One-to-one or group if applicable",
    )
    tax_rate = models.ForeignKey(
        "taxes.Tax",
        blank=False,
        null=False,
        on_delete=models.PROTECT,
        related_name="product_services",
        help_text=_("Required. Must set correctly."),
    )
    price_summary = models.CharField(
        _("Current Price(s) (￥)"),
        null=False,
        blank=False,
        editable=False,
        max_length=100,
        help_text="Autogenerated",
    )
    description = models.TextField(
        _("Product Description"),
        null=False,
        blank=False,
        help_text="Required. Base description of product. Any changes here should be reflected in any display page or language",
    )
    min_num = models.PositiveSmallIntegerField(
        _("Min Num People"),
        null=True,
        blank=True,
        help_text="NOT Required. Min Number of people if applicable",
    )
    max_num = models.PositiveSmallIntegerField(
        _("Max Num People"),
        null=True,
        blank=True,
        help_text="NOT Required. Max Number of people if applicable",
    )
    length = models.PositiveSmallIntegerField(
        _("Length"),
        null=True,
        blank=True,
        help_text="NOT Required. Length of class or experience if applicable. Example. Number of Minutes or number of words",
    )
    length_unit = models.CharField(
        _("Class Length Unit"),
        null=False,
        blank=False,
        max_length=20,
        default=LengthUnitChoices.NA,
        choices=LengthUnitChoices.choices,
        help_text="Required. Unit by which length is measured. Example. Minutes or words",
    )
    quantity = models.PositiveSmallIntegerField(
        _("Quantity"),
        null=True,
        blank=True,
        help_text="NOT Required. Quantity if applicable (Per Unit) ",
    )
    quantity_unit = models.CharField(
        _("Quantity Unit"),
        null=False,
        blank=False,
        max_length=20,
        default=QuantityUnitChoices.NA,
        choices=QuantityUnitChoices.choices,
        help_text="Required. Unit by which quantity is measured. Example. Month or Payment",
    )
    is_native = models.BooleanField(
        _("Is Native"),
        null=True,
        blank=False,
        help_text="NOT Required. Is run by a native language speaker if applicable?",
    )
    is_online = models.BooleanField(
        _("Is Online"),
        null=True,
        blank=False,
        help_text="NOT Required. Is able to be taken online if applicable?",
    )
    is_inperson = models.BooleanField(
        _("Is Inperson"),
        null=True,
        blank=False,
        help_text="NOT Required. Is able to be taken in person if applicable?",
    )
    has_onlinenotes = models.BooleanField(
        _("Has Online Notes"),
        null=True,
        blank=False,
        help_text="NOT Required. Has onlinenotes if applicable ?",
    )
    bookable_online = models.BooleanField(
        _("Bookable online"),
        null=True,
        blank=False,
        help_text="NOT Required. Can be booked online if applicable",
    )
    # Class specific fields
    class_type = models.CharField(
        _("Class Type"),
        null=False,
        blank=False,
        max_length=20,
        default=ClassTypeChoices.NA,
        choices=ClassTypeChoices.choices,
        help_text="Class field only. Class composition is controlled privately or by Xlingual",
    )

    def __str__(self):
        return self.name

    def _get_slug_or_raise_custom_error(self):
        slug = slugify(self.name)
        unique_slug = slug

        if not ProductService.objects.filter(slug=unique_slug).exists():
            return unique_slug
        else:
            # Is own slug
            if ProductService.objects.filter(slug=unique_slug)[0].id == self.id:
                return unique_slug

            else:
                similar_object = ProductService.objects.filter(slug=unique_slug)[0]
                raise ValidationError(
                    f"The slug value {unique_slug} indicates this product is not unique. It is similar to the product with name: {similar_object.name}  and id:  {similar_object.id}"
                )

    def clean(self):
        self.slug = self._get_slug_or_raise_custom_error()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class ProductServicePrice(TimeStampedModel):
    product_service = models.ForeignKey(
        ProductService,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name="prices",
    )
    name = models.CharField(
        _("Name"),
        blank=False,
        null=False,
        max_length=200,
        help_text=_("Required. Max length 200 characters. In English please."),
    )
    display_name = models.CharField(
        _("Display Name"),
        blank=False,
        null=False,
        max_length=200,
        help_text=_(
            "Required. Max length 200 characters. Will in many cases be Japanese name."
        ),
    )
    price = models.DecimalField(
        _("Price"),
        blank=False,
        null=False,
        max_digits=10,
        decimal_places=0,
        validators=[MinValueValidator(Decimal("0"))],
        help_text=_("Required. Pretax selling price in Japanese yen. Max digits - 10"),
    )
    start_date = models.DateTimeField(
        _("Start date"),
        blank=False,
        null=False,
        help_text="Required. Please make sure to set this. It is generally never changed",
    )
    is_limited_sale = models.BooleanField(
        _("Is Limited Sale Price"),
        blank=False,
        null=False,
        default=False,
        help_text="If ticked, please make sure to add the end date",
    )
    before_sale_price = models.DecimalField(
        _("Before Sale Pretax Price"),
        blank=True,
        null=True,
        max_digits=10,
        decimal_places=0,
        validators=[MinValueValidator(Decimal("0"))],
        help_text=_(
            "NOT Required. Only enter this price for 'is_limited_sale' prices. It will show up with line through on any front end display to indicate that price has been cut for the limited time"
        ),
    )
    end_date = models.DateTimeField(
        _("End date"),
        blank=True,
        null=True,
        help_text="NOT Required. Important ** Do not set this for long term prices. It is only used to have a short sale price or to terminate a long term price. It will remove the price from any public display if the current date is later than the end date",
    )

    def __str__(self):
        return f"{self.name} (￥{self.price})"


class LearningExperience(TimeStampedModel):
    """Base Model for a learning experience"""

    name = models.CharField(
        _("Name"),
        blank=False,
        null=False,
        max_length=200,
        help_text=_("Required. Max length 200 characters."),
    )
    product_service = models.ForeignKey(
        ProductService,
        blank=False,
        null=False,
        on_delete=models.PROTECT,
        related_name="learningexperiences",
        limit_choices_to={"ptype": "experience"},
        help_text=_("Required."),
    )
    start_date = models.DateField(
        _("Start Date"),
        blank=False,
        null=False,
        help_text=_("Required."),
    )
    end_date = models.DateField(
        _("End Date"),
        blank=False,
        null=False,
        help_text=_("Required."),
    )
    max_people = models.PositiveSmallIntegerField(
        _("Max People"),
        blank=False,
        null=False,
        default=0,
        help_text=_("Required."),
    )
    total_attended = models.PositiveSmallIntegerField(
        _("Total People"),
        blank=False,
        null=False,
        default=0,
        help_text=_("Required."),
    )
    total_new = models.PositiveSmallIntegerField(
        _("New people"),
        blank=False,
        null=False,
        default=0,
        help_text=_("Required."),
    )
    total_profit = models.DecimalField(
        _("Total Profit (￥)"),
        blank=False,
        null=False,
        max_digits=10,
        decimal_places=0,
        default=Decimal("0"),
        validators=[MinValueValidator(Decimal("0"))],
        help_text=_("Required. Basic, revenue - total costs including teacher time."),
    )

    def __str__(self):
        return f"{self.start_date} | {self.name}"


# =====================
# Display Page Models and field serializers
# =====================
class LearningExperienceListPage(HeadlessMixin, Page):
    display_title = models.CharField(
        "Display Title",
        blank=False,
        null=False,
        max_length=15,
        help_text="Required. Max length 15 characters. Japanese",
    )
    intro = RichTextField(
        "LE - Intro",
        blank=False,
        null=False,
        features=[
            "bold",
            "link",
        ],
        help_text="Required. For the concepts surrounding learning experiences",
    )
    # Upcoming experiences
    upcoming_en_title = models.CharField(
        "LE - Upcoming English title",
        blank=False,
        null=False,
        max_length=25,
        help_text="Required. Max length 25, 15 or less is ideal",
    )
    upcoming_jp_title = models.CharField(
        "Mission - Japanese Title",
        blank=False,
        null=False,
        max_length=20,
        help_text="Required. Max length 20 characters, 15 or less is ideal",
    )

    # Experiences gallery
    gallery_en_title = models.CharField(
        "LE - Gallery English title",
        blank=False,
        null=False,
        max_length=25,
        help_text="Required. Max length 25, 15 or less is ideal",
    )
    gallery_jp_title = models.CharField(
        "LE - Japanese Title",
        blank=False,
        null=False,
        max_length=20,
        help_text="Required. Max length 20 characters, 15 or less is ideal",
    )
    experiences_gallery = StreamField(
        [
            (
                "simple_image_block",
                customblocks.SimpleImageBlock(),
            ),
        ],
        use_json_field=True,
        null=True,
        blank=False,
        min_num=4,
        max_num=20,
    )
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("display_title"),
                FieldPanel("intro"),
            ],
            heading="Learning Experience header section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("upcoming_en_title"),
                FieldPanel("upcoming_jp_title"),
            ],
            heading="Learning Experience upcoming section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("gallery_en_title"),
                FieldPanel("gallery_jp_title"),
                FieldPanel("experiences_gallery"),
            ],
            heading="Learning Experience gallery section",
        ),
    ]

    api_fields = [
        APIField("display_title"),
        APIField("intro"),
        APIField("upcoming_en_title"),
        APIField("upcoming_jp_title"),
        APIField("gallery_en_title"),
        APIField("gallery_jp_title"),
        APIField("experiences_gallery"),
    ]

    # Page limitations, Meta and methods
    max_count = 1
    parent_page_types = [
        "home.HomePage",
    ]

    def __str__(self):
        return self.title


# ================================
# Detail Page and Field Serializers
# ================================


class LESerializer(Field):
    def calculate_taxed_amount(self, price, tax_rate):
        if not isinstance(price, Decimal) or not isinstance(tax_rate, Decimal):
            return None
        return str(round(price + (price * (tax_rate / Decimal("100.00")))))

    def to_representation(self, value):
        prices = []
        tax_rate = value.product_service.tax_rate.rate
        for p in value.product_service.prices.all():
            price_dict = {
                "id": p.id,
                "name": p.name,
                "display_name": p.display_name,
                "pretax_price": str(p.price),
                "posttax_price": self.calculate_taxed_amount(p.price, tax_rate),
                "start_date": p.start_date,
                "is_limited_sale": p.is_limited_sale,
                "before_sale_pretax_price": p.before_sale_price,
                "before_sale_posttax_price": self.calculate_taxed_amount(
                    p.before_sale_price, tax_rate
                ),
                "end_date": p.end_date,
            }
            prices.append(price_dict)

        return {
            "id": value.id,
            "name": value.name,
            "start_date": value.start_date,
            "end_date": value.end_date,
            "product_service": {
                "id": value.product_service.id,
                "name": value.product_service.name,
                "tax_rate": tax_rate,
                "prices": prices,
            },
        }


class StaffMembersFieldSerializer(Field):
    def to_representation(self, value):
        image = value.profile_image
        return {
            "id": value.id,
            "name": value.title,
            "slug": value.slug,
            "position": value.role,
            "intro": value.intro,
            "image": {
                "id": image.id,
                "title": image.title,
                "original": image.get_rendition("original").attrs_dict,
                "thumbnail": image.get_rendition("fill-450x450").attrs_dict,
            },
        }


class ExperienceAddressFieldSerializer(Field):
    def to_representation(self, value):
        return {
            "id": value.id,
            "name": value.name,
            "display_name": value.display_name,
            "line_one": value.line_one,
            "line_two": value.line_two,
            "city_town_village": value.city_town_village,
            "postal_code": value.postal_code,
            "country": value.get_country_display(),
        }


class LearningExperienceDetailPage(HeadlessMixin, Page):
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
        help_text="Required. Max length 160 char. A catchy, attractive tagline to give more information and sell the experience",
    )
    learning_experience = models.OneToOneField(
        LearningExperience,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        help_text="The associated learning experience",
    )
    header_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        related_name="+",
        help_text="Image size: 2048px x 1280px. Please optimize image size before uploading.",
    )
    start_date = models.DateField(
        "Start Date",
        blank=True,
        null=False,
        help_text="Read only field that gets value from 'learning_experience'",
    )
    end_date = models.DateField(
        "End Date",
        blank=True,
        null=False,
        help_text="Read only field that gets value from 'learning_experience'",
    )
    will_do = RichTextField(
        "What you will do",
        blank=False,
        null=False,
        features=[
            "h3",
            "h4",
            "bold",
            "italic",
            "ol",
            "ul",
        ],
        help_text="Required. Include how this helps language learning",
    )
    past_photos = StreamField(
        [
            (
                "simple_image_block",
                customblocks.SimpleImageBlock(),
            ),
        ],
        use_json_field=True,
        null=True,
        blank=False,
        min_num=4,
    )
    details = StreamField(
        [
            (
                "limited_rich_text_block",
                customblocks.CustomLimitedRichTextBlock(),
            ),
            (
                "schedule_block",
                customblocks.ScheduleBlock(),
            ),
        ],
        use_json_field=True,
        null=True,
        blank=False,
    )
    display_map = models.TextField(
        "Display map",
        null=False,
        blank=False,
        help_text='Required. Please paste the iframe imbed code here. Please remove both the height="....." and width="....." attributes from the code before saving otherwise the map will not display as intended on the site',
    )
    address = models.ForeignKey(
        "addresses.ExperienceAddress",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Not required but preferable if applicable",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("display_title"),
                FieldPanel("display_tagline"),
                FieldPanel("learning_experience"),
                FieldPanel("header_image"),
                FieldPanel("start_date", read_only=True),
                FieldPanel("end_date", read_only=True),
            ],
            heading="Header section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("will_do"),
                InlinePanel("staff_members", label="Staff Member"),
                FieldPanel("past_photos"),
            ],
            heading="Will do, staff and past photos",
        ),
        MultiFieldPanel(
            [
                FieldPanel("details"),
            ],
            heading="Details and schedules",
        ),
        MultiFieldPanel(
            [
                FieldPanel("display_map"),
                FieldPanel("address"),
            ],
            heading="Maps and address",
        ),
        MultiFieldPanel(
            [
                InlinePanel("related_lessons", label="Lesson", max_num=4),
            ],
            heading="Related Lessons",
        ),
    ]

    api_fields = [
        APIField("display_title"),
        APIField("display_tagline"),
        APIField("learning_experience", serializer=LESerializer()),
        APIField("header_image", serializer=HeaderImageFieldSerializer()),
        APIField("start_date"),
        APIField("end_date"),
        APIField("will_do"),
        APIField("staff_members"),
        APIField("past_photos"),
        APIField("details"),
        APIField("display_map"),
        APIField("address", serializer=ExperienceAddressFieldSerializer()),
        APIField("related_lessons"),
    ]

    # Page limitations, Meta and methods
    parent_page_types = [
        "products.LearningExperienceListPage",
    ]

    def __str__(self):
        return self.title

    def clean(self):
        """Custom clean method to make start_date and end_date duplicate learning experience fields of same name. This denormalization and duplication is to reduce queries the list views"""
        if not self.start_date == self.learning_experience.start_date:
            self.start_date = self.learning_experience.start_date
        if not self.end_date == self.learning_experience.end_date:
            self.end_date = self.learning_experience.end_date


class ExperiencePageStaff(Orderable):
    page = ParentalKey(
        LearningExperienceDetailPage,
        on_delete=models.CASCADE,
        related_name="staff_members",
    )
    staff = models.ForeignKey(
        "staff.StaffDetailPage",
        on_delete=models.CASCADE,
    )
    # Panels

    panels = [
        FieldPanel("staff"),
    ]

    api_fields = [
        APIField("staff", serializer=StaffMembersFieldSerializer()),
    ]

    def __str__(self):
        return self.staff.title


class ExperienceRelatedLessons(Orderable):
    """Orderable field for lessons that should be connected to this learing experience"""

    page = ParentalKey(
        LearningExperienceDetailPage,
        on_delete=models.CASCADE,
        related_name="related_lessons",
    )
    lesson = models.ForeignKey("lessons.LessonDetailPage", on_delete=models.CASCADE)

    panels = [
        FieldPanel("lesson"),
    ]

    api_fields = [
        APIField("lesson", serializer=LessonRelatedFieldSerializer()),
    ]


# ===========================
# Class Product and Prices
# ===========================


class ClassPricesListPage(HeadlessMixin, Page):
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
        help_text="Required. Max length 160 char. A catchy, attractive tagline to give more information and sell the classes",
    )
    intro = RichTextField(
        "Introduction",
        blank=False,
        null=False,
        features=[
            "h3",
            "h4",
            "bold",
            "italic",
            "ol",
            "ul",
        ],
        help_text="Required. For the concepts surrounding Xlingual classes",
    )
    private_title = models.CharField(
        "Private Classes Title",
        blank=False,
        null=False,
        max_length=100,
        help_text="Required. Max length 100 characters, 45 or less is ideal",
    )
    private_tagline = models.CharField(
        "Private Classes Tagline",
        blank=False,
        null=False,
        max_length=160,
        help_text="Required. Max length 160 char. A catchy, attractive tagline to give more information and sell the classes",
    )
    private_intro = RichTextField(
        "Private Classes Introduction",
        blank=False,
        null=False,
        features=[
            "h3",
            "h4",
            "bold",
            "italic",
            "ol",
            "ul",
        ],
        help_text="Required. For the concepts surrounding Xlingual private classes. Not too long please",
    )
    regular_title = models.CharField(
        "Regular Classes Title",
        blank=False,
        null=False,
        max_length=100,
        help_text="Required. Max length 100 characters, 45 or less is ideal",
    )
    regular_tagline = models.CharField(
        "Regular Classes Tagline",
        blank=False,
        null=False,
        max_length=160,
        help_text="Required. Max length 160 char. A catchy, attractive tagline to give more information and sell the classes",
    )
    regular_intro = RichTextField(
        "Regular Classes Introduction",
        blank=False,
        null=False,
        features=[
            "h3",
            "h4",
            "bold",
            "italic",
            "ol",
            "ul",
        ],
        help_text="Required. For the concepts surrounding Xlingual private classes. Not too long please",
    )
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("display_title"),
                FieldPanel("display_tagline"),
                FieldPanel("intro"),
            ],
            heading="Class Prices header section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("private_title"),
                FieldPanel("private_tagline"),
                FieldPanel("private_intro"),
            ],
            heading="Private Classes section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("regular_title"),
                FieldPanel("regular_tagline"),
                FieldPanel("regular_intro"),
            ],
            heading="Regular Classes section",
        ),
    ]

    api_fields = [
        APIField("display_title"),
        APIField("display_tagline"),
        APIField("intro"),
        APIField("private_title"),
        APIField("private_tagline"),
        APIField("private_intro"),
        APIField("regular_title"),
        APIField("regular_tagline"),
        APIField("regular_intro"),
    ]

    # Page limitations, Meta and methods
    max_count = 1
    parent_page_types = [
        "home.HomePage",
    ]

    def __str__(self):
        return self.title


class ClassServiceFieldSerializer(Field):
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
        return {
            "id": value.id,
            "name": value.name,
            "slug": value.slug,
            "class_type": value.class_type,
            "class_type_display": value.get_class_type_display(),
            "min_num": value.min_num,
            "max_num": value.max_num,
            "length": value.length,
            "length_unit": value.get_length_unit_display(),
            "quantity": value.quantity,
            "quantity_unit": value.get_quantity_unit_display(),
            "is_native": value.is_native,
            "is_online": value.is_online,
            "is_inperson": value.is_inperson,
            "has_onlinenotes": value.has_onlinenotes,
            "bookable_online": value.bookable_online,
            "price_info": self.get_price(value.prices.all(), value.tax_rate.rate),
        }


class ClassPricesDetailPage(HeadlessMixin, Page):
    class_service = models.OneToOneField(
        ProductService,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        limit_choices_to={"ptype": "class"},
        help_text="The associated class. Title of this page should match the name of this associated class product. If it doesn't the title will be updated to match on save.",
    )
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
        help_text="Required. Max length 160 char. A catchy, attractive tagline to give more information and sell the class",
    )
    header_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        related_name="+",
        help_text="Image size: 2048px x 1280px. Please optimize image size before uploading.",
    )
    class_intro = StreamField(
        [
            ("rich_text", customblocks.CustomRichTextBlock()),
            ("beyond_text_img", customblocks.StandardCustomImageBlock()),
            ("text_width_img", customblocks.StandardCustomImageBlock()),
            ("youtube", customblocks.YoutubeBlock()),
        ],
        use_json_field=True,
        null=True,
        blank=False,
    )
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("class_service"),
                FieldPanel("display_title"),
                FieldPanel("display_tagline"),
                FieldPanel("header_image"),
            ],
            heading="Class Prices header section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("class_intro"),
            ],
            heading="Class sales section",
        ),
    ]

    api_fields = [
        APIField("class_service", serializer=ClassServiceFieldSerializer()),
        APIField("display_title"),
        APIField("display_tagline"),
        APIField("header_image", serializer=HeaderImageFieldSerializer()),
        APIField("class_intro"),
    ]

    # Page limitations, Meta and methods
    parent_page_types = [
        "products.ClassPricesListPage",
    ]

    def __str__(self):
        return self.title

    def clean(self):
        """Custom clean method to make sure that title and slug are the same as productservice"""
        if not self.title == self.class_service.name:
            self.title = self.class_service.name
        if not self.slug == self.class_service.slug:
            self.slug = self.class_service.slug
