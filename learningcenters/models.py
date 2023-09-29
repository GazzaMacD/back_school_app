from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.api import APIField
from rest_framework.fields import Field
from streams import customblocks

from core.models import (
    TimeStampedModel,
)
from core.serializers import HeaderImageFieldSerializer


# Field Serializers
class LCSerializer(Field):
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
class LearningCenter(TimeStampedModel):
    """Learning Center base model"""

    name = models.CharField(
        _("name"),
        blank=True,
        null=False,
        max_length=100,
        help_text="Name of the learning center in English. Will be used as the name for the public page title.",
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
        help_text="This address will be used in public facing displays. Please make sure to mark 'is_learning_center' as true if entering a new address",
    )

    def __str__(self) -> str:
        return self.name


class LearningCenterListPage(Page):
    """Display list page for the all learning centers"""

    display_title = models.CharField(
        "Display Title",
        blank=False,
        null=False,
        max_length=100,
        help_text="Required. Max length 100 characters, 45 or less is ideal",
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
            heading="LC List Page header section",
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


class LearningCenterDetailPage(Page):
    """Display page for the learning center"""

    display_title = models.CharField(
        "Display Title",
        blank=False,
        null=False,
        max_length=100,
        help_text="Required. Max length 100 characters, 45 or less is ideal",
    )
    lc = models.ForeignKey(
        "learningcenters.LearningCenter",
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        help_text="The associated learning center. Title of this page should match the name of this associated learning center. If it doesn't the title will be updated to match on save.",
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
        help_text="Required.",
    )
    display_map = models.TextField(
        "Display map",
        null=False,
        blank=False,
        help_text='Required. Please paste the iframe imbed code here. Please remove both the height="....." and width="....." attributes from the code before saving otherwise the map will not display as intended on the site',
    )
    access_info = models.TextField(
        "Access Information",
        null=False,
        blank=False,
        help_text="Please explain all modes of access relevent to this lc",
    )
    lc_photos = StreamField(
        [
            ("si_block", customblocks.SimpleImageBlock()),
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
                FieldPanel("lc"),
                FieldPanel("header_image"),
                FieldPanel("display_intro"),
            ],
            heading="Language Center header section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("display_map"),
                FieldPanel("access_info"),
            ],
            heading="Language Location and Access",
        ),
        MultiFieldPanel(
            [
                FieldPanel("lc_photos"),
            ],
            heading="Language Center Photos",
        ),
    ]
    # Api configuration
    api_fields = [
        APIField("display_title"),
        APIField("lc", serializer=LCSerializer()),
        APIField("header_image", serializer=HeaderImageFieldSerializer()),
        APIField("display_intro"),
        APIField("display_map"),
        APIField("access_info"),
        APIField("lc_photos"),
    ]

    # Page limitations, Meta and methods
    parent_page_types = [
        "learningcenters.LearningCenterListPage",
    ]

    def __str__(self):
        return self.title

    def full_clean(self, *args, **kwargs):
        """Use full clean to manipulate title and slug so as to be consistent
        with the base language center django model"""
        super().full_clean(*args, **kwargs)

        if not self.title == self.lc.name:
            self.title = self.lc.name

        if not self.slug == self.lc.slug:
            self.slug = self.lc.slug
