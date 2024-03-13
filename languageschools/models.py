from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.api import APIField
from wagtail_headless_preview.models import HeadlessMixin
from rest_framework.fields import Field

from streams import customblocks
from core.models import (
    TimeStampedModel,
)
from core.serializers import HeaderImageFieldSerializer


# Field Serializers
class LSSerializer(Field):
    def to_representation(self, value):
        ad = value.address
        return {
            "id": value.id,
            "name": value.name,
            "address": {
                "line_one": ad.line_one,
                "line_two": ad.line_two,
                "city": ad.city_town_village,
                "state": ad.prefecture_state,
                "code": ad.postal_code,
                "country": ad.get_country_display(),
            },
        }


# Models
class LanguageSchool(TimeStampedModel):
    """Language School base model"""

    name = models.CharField(
        _("name"),
        blank=True,
        null=False,
        max_length=100,
        help_text="Name of the language school in English. Will be used as the name for the public page title.",
    )
    slug = models.SlugField(
        _("Slug"),
        blank=False,
        null=False,
        unique=True,
        max_length=100,
        help_text="Slug must be all lower case and separated by hyphens if necessary. This slug value will be used in the public urls",
    )
    address = models.ForeignKey(
        "addresses.Address",
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        help_text="This address will be used in public facing displays. Please make sure to mark 'is_language_school' as true if entering a new address",
    )

    def __str__(self) -> str:
        return self.name


class LanguageSchoolListPage(HeadlessMixin, Page):
    """Display list page for all language schools"""

    # Fields
    display_title = models.CharField(
        "Display Title",
        blank=False,
        null=False,
        max_length=15,
        help_text="Required. Max length 15 characters. Japanese",
    )
    display_intro = RichTextField(
        "Display Introduction",
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
        help_text="Required.",
    )

    # Admin panel configuration
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("display_title"),
                FieldPanel("display_intro"),
            ],
            heading="Header Section",
        ),
    ]

    # Api configuration
    api_fields = [
        APIField("display_title"),
        APIField("display_intro"),
    ]

    # Page limitations, Meta and methods
    max_count = 1
    parent_page_types = [
        "home.HomePage",
    ]

    def __str__(self):
        return self.title


class LanguageSchoolDetailPage(HeadlessMixin, Page):
    """Detail display page for the language school"""

    display_title = models.CharField(
        "Display Title",
        blank=False,
        null=False,
        max_length=15,
        help_text="Required. Max length 15 characters. Japanese",
    )
    display_tagline = models.CharField(
        "Display tagline",
        blank=False,
        null=False,
        max_length=50,
        help_text="Required. Max 50. Attractive, short summary of school",
    )
    ls = models.ForeignKey(
        "languageschools.LanguageSchool",
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        help_text="The associated language school. Title of this page should match the name of this associated language school. If it doesn't the title and slug will be updated to match on save.",
    )
    header_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        related_name="+",
        help_text="Image size: 2048px x 1280px. Please optimize image size before uploading.",
    )
    display_intro = RichTextField(
        "Display Introduction",
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
        help_text="Required. Introduction to the school",
    )
    display_map = models.TextField(
        "Display map",
        null=False,
        blank=False,
        help_text='Required. Please paste the iframe imbed code here. Please remove both the height="....." and width="....." attributes from the code before saving otherwise the map will not display as intended on the site',
    )
    display_city = models.CharField(
        "Readonly Display City",
        null=False,
        blank=True,
        help_text="Readonly Field, auto updated from school address. If address is changed in admin please save this again to update this field",
    )
    access_train = models.CharField(
        "Access - Train",
        null=False,
        blank=False,
        max_length=35,
        help_text="Required. Max 35char. Please explain in Japanese train access",
    )
    access_car = models.CharField(
        "Access - Car",
        null=False,
        blank=False,
        max_length=35,
        help_text="Required. Max 35char. Please explain in Japanese car access and whether parking is available or not",
    )
    ls_photos = StreamField(
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

    # Admin panel configuration
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("display_title"),
                FieldPanel("display_tagline"),
                FieldPanel("ls"),
                FieldPanel("header_image"),
                FieldPanel("display_intro"),
            ],
            heading="Header Section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("display_map"),
                FieldPanel("display_city", read_only=True),
                FieldPanel("access_train"),
                FieldPanel("access_car"),
            ],
            heading="Access",
        ),
        MultiFieldPanel(
            [
                FieldPanel("ls_photos"),
            ],
            heading="School Photos",
        ),
    ]
    # Api configuration
    api_fields = [
        APIField("display_title"),
        APIField("display_tagline"),
        APIField("ls", serializer=LSSerializer()),
        APIField("header_image", serializer=HeaderImageFieldSerializer()),
        APIField("display_intro"),
        APIField("display_map"),
        APIField("display_city"),
        APIField("access_train"),
        APIField("access_car"),
        APIField("ls_photos"),
    ]

    # Page limitations, Meta and methods
    parent_page_types = [
        "languageschools.LanguageSchoolListPage",
    ]

    def __str__(self):
        return self.title

    def clean(self):
        """Custom clean to manipulate title and slug so as to be consistent
        with the base language school django model. Also to update the display_city
         field to be consistend with school address. To save queries on list views"""
        if not self.title == self.ls.name:
            self.title = self.ls.name

        if not self.slug == self.ls.slug:
            self.slug = self.ls.slug

        if not self.display_city == self.ls.address.city_town_village:
            self.display_city = self.ls.address.city_town_village
