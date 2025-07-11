from decimal import Decimal
from datetime import date

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.utils.text import slugify

from wagtail.api import APIField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Page
from wagtail_headless_preview.models import HeadlessMixin
from wagtail.fields import RichTextField, StreamField

from core.serializers import HeaderImageFieldSerializer
from streams import customblocks
from core.models import TimeStampedModel


# Helpers
def get_campaign_slug(title, start_date, end_date):
    """Create campaign slug using title and dates"""
    start = f"{start_date:%Y-%m-%d}"
    end = f"{end_date:%Y-%m-%d}"
    return f"{slugify(title, allow_unicode=True)}-{start}-to-{end}"


def default_marketing_start():
    d = date(2020, 1, 1)
    return d


# Django Campaign Models

CAMPAIGN_DESC_DEFAULT = """[BRIEF]\n
[SMART GOALS]\n
S: \n
M: \n
A: \n
R: \n
T: \n
[CHANNELS TO BE USED]\n
"""


class Campaign(TimeStampedModel):
    """Base model for all campaigns created for organization"""

    name = models.CharField(
        _("Name"),
        blank=False,
        null=False,
        max_length=100,
        help_text="Required. 100 Char max. Campaign name in English",
    )
    marketing_start_date = models.DateField(
        _("Marketing Start Date"),
        blank=False,
        null=False,
        default=default_marketing_start,
        help_text="Required. This will determine the visibility of the campaign once the CMS page has been created",
    )
    start_date = models.DateField(
        _("Start Date"),
        blank=False,
        null=False,
        help_text="Required",
    )
    end_date = models.DateField(
        _("End Date"),
        blank=False,
        null=False,
        help_text="Required",
    )
    description = models.TextField(
        _("Campaign Description"),
        blank=False,
        null=False,
        default=CAMPAIGN_DESC_DEFAULT,
        help_text="Description of key elements of campaign. Please use SMART here.",
    )
    target_total_customer_increase = models.PositiveSmallIntegerField(
        _("Target Cust. Inc."),
        blank=False,
        null=False,
        default=0,
        help_text="Required. Complete 'Target Customer Increase' before the campaign start date",
    )
    total_customer_increase = models.PositiveSmallIntegerField(
        _("Total Cust. Inc."),
        blank=False,
        null=False,
        default=0,
        help_text="Required. Update 'Actual Total Customer Increase' as results appear",
    )
    target_monthly_recurring_revenue_increase = models.DecimalField(
        _("Target Rev Inc. (￥)"),
        blank=False,
        null=False,
        max_digits=10,
        decimal_places=0,
        default=Decimal("0"),
        validators=[MinValueValidator(Decimal("0"))],
        help_text="Required. Complete 'Target Monthly Recurring Revenue Increase' before the campaign start date",
    )
    monthly_recurring_revenue_increase = models.DecimalField(
        _("Monthly Rec Rev Increase (￥)"),
        blank=False,
        null=False,
        max_digits=10,
        decimal_places=0,
        default=Decimal("0"),
        validators=[MinValueValidator(Decimal("0"))],
        help_text="Required. Update 'Actual Monthly Recurring Revenue Increase' as results come in",
    )
    smart_goals_achieved = models.BooleanField(
        _("Smart Goals Achieved"),
        blank=False,
        null=False,
        default=False,
        help_text="Required. Completed after campaign results finalized. Please consider 'M' in SMART to answer this question",
    )
    note = models.TextField(
        _("Campaign Note"),
        blank=True,
        null=False,
        help_text="Notes regarding this campaign if any",
    )

    def __str__(self) -> str:
        return self.name


# =====================
# Wagtail Campaign Page Models
# =====================


class CampaignListPage(HeadlessMixin, Page):
    """List page acting ass parent for all campaign detail models. Currently (08.2024) not displayed on front end"""

    display_title = models.CharField(
        "Display Title",
        blank=False,
        null=False,
        max_length=20,
        help_text="Required. Max length 20 characters. Japanese",
    )

    # Admin panel configuration
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("display_title"),
            ],
            heading="Header Section ",
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

    def __str__(self) -> str:
        return self.title


# ======= Simple Banner Page ===========
class ColorTypeChoices(models.TextChoices):
    LIGHT_BLUE = "lightblue", "Light Blue"


class CampaignSimpleBannerPage(HeadlessMixin, Page):
    """A page class representing a simple text based banner for campaign banners. Has a mandatory 'type' field to allow front end to determine display components based on this type. This particluar model also has a choice of color types which will determine the design colors on the front for this 'type' of campaign page"""

    campaign = models.OneToOneField(
        Campaign,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        help_text="The associated campaign. IMPORTANT. PLease make sure the title on this page is the same as the campaign name.",
    )
    campaign_page_type = models.CharField(
        _("Campaign Page Type"),
        blank=False,
        null=False,
        default="simple_banner",
        editable=False,
        max_length=20,
        help_text="Auto generated",
    )
    color_type = models.CharField(
        _("Banner Color"),
        null=False,
        blank=False,
        max_length=10,
        choices=ColorTypeChoices.choices,
        help_text="Required. Will determine the color scheme of the banner and page",
    )
    name_ja = models.CharField(
        "Japanese Campaign Name",
        blank=False,
        null=False,
        max_length=18,
        help_text="Required. Max length 18 chars. Will be name of campaign on banner. Please avoid using 'キャンペーン' in the name. It is already on the banner below this name.",
    )
    offer = models.CharField(
        "Campaign Offer",
        blank=False,
        null=False,
        max_length=20,
        help_text="Required. Max length 20 chars. The offer, biggest text on the banner",
    )
    tagline = models.CharField(
        "Tagline",
        blank=False,
        null=False,
        max_length=100,
        help_text="Required. Max length 100 chars. Succint additional text to add marketing value to the banner",
    )
    marketing_start_date = models.DateField(
        "Marketing Start Date",
        blank=True,
        null=False,
        help_text="Read only field that gets value from 'campaign'",
    )
    start_date = models.DateField(
        "Start Date",
        blank=True,
        null=False,
        help_text="Read only field that gets value from 'campaign'",
    )
    end_date = models.DateField(
        "End Date",
        blank=True,
        null=False,
        help_text="Read only field that gets value from 'campaign'",
    )
    additional_details = RichTextField(
        _("Additional details"),
        blank=False,
        null=False,
        features=[
            "link",
            "h3",
            "h4",
            "bold",
            "italic",
            "ol",
            "ul",
        ],
        help_text="Required. Please add any additional info here. Conditions links etc",
    )

    # Admin panel configuration
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("campaign"),
                FieldPanel("campaign_page_type", read_only=True),
                FieldPanel("color_type"),
            ],
            heading="Core Information",
        ),
        MultiFieldPanel(
            [
                FieldPanel("name_ja"),
                FieldPanel("offer"),
                FieldPanel("tagline"),
                FieldPanel("marketing_start_date", read_only=True),
                FieldPanel("start_date", read_only=True),
                FieldPanel("end_date", read_only=True),
            ],
            heading="Banner Info",
        ),
        MultiFieldPanel(
            [
                FieldPanel("additional_details"),
            ],
            heading="More Info",
        ),
    ]

    # Api configuration
    api_fields = [
        APIField("campaign_page_type"),
        APIField("color_type"),
        APIField("name_ja"),
        APIField("offer"),
        APIField("tagline"),
        APIField("marketing_start_date"),
        APIField("start_date"),
        APIField("end_date"),
        APIField("additional_details"),
    ]

    # Page limitations, Meta and methods
    parent_page_types = [
        "campaigns.CampaignListPage",
    ]

    def __str__(self) -> str:
        return self.title

    def clean(self):
        """Custom clean method to make start_date and end_date duplicate learning experience fields of same name. This denormalization and duplication is to reduce queries in the list views. Construct the slug string and replace auto generated slug with this string"""
        if not self.marketing_start_date == self.campaign.marketing_start_date:
            self.marketing_start_date = self.campaign.marketing_start_date
        if not self.start_date == self.campaign.start_date:
            self.start_date = self.campaign.start_date
        if not self.end_date == self.campaign.end_date:
            self.end_date = self.campaign.end_date

        # Make campaign model title and this display model title consistent
        if not self.title == self.campaign.name:
            self.title = self.campaign.name

        # Construct slug stringo
        slug = get_campaign_slug(self.title, self.start_date, self.end_date)
        if not self.slug == slug:
            self.slug = slug


# ======= Image Banner  Page ===========


class CampaignImageBannerPage(HeadlessMixin, Page):
    """A page class representing a campaign with an Image as the main banner. Has a mandatory 'type' field to allow front end to determine display components based on this type."""

    campaign = models.OneToOneField(
        Campaign,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        help_text="The associated campaign. IMPORTANT. PLease make sure the title on this page is the same as the campaign name.",
    )
    campaign_page_type = models.CharField(
        _("Campaign Page Type"),
        blank=False,
        null=False,
        default="image_banner",
        editable=False,
        max_length=20,
        help_text="Auto generated",
    )
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        related_name="+",
        help_text="Image size: 2048px x 1280px. Please optimize image size before uploading.",
    )
    name_ja = models.CharField(
        "Japanese Campaign Name",
        blank=False,
        null=False,
        max_length=18,
        help_text="Required. Max length 18 chars. Will be name of campaign displayed in the title tag for the page ",
    )
    tagline = models.CharField(
        "Tagline",
        blank=False,
        null=False,
        max_length=100,
        help_text="Required. Max length 100 chars. Succint additional Japanese text to add marketing value to the description tag",
    )
    marketing_start_date = models.DateField(
        "Marketing Start Date",
        blank=True,
        null=False,
        help_text="Read only field that gets value from 'campaign'. Will determine when the page is visible on the home page and other places on site",
    )
    start_date = models.DateField(
        "Start Date",
        blank=True,
        null=False,
        help_text="Read only field that gets value from 'campaign'",
    )
    end_date = models.DateField(
        "End Date",
        blank=True,
        null=False,
        help_text="Read only field that gets value from 'campaign'",
    )
    additional_details = StreamField(
        [
            ("rich_text", customblocks.CustomRichTextBlock()),
            ("text_width_img", customblocks.StandardCustomImageBlock()),
            ("youtube", customblocks.YoutubeBlock()),
            ("show_hide", customblocks.ShowHideBlock()),
        ],
        use_json_field=True,
        null=True,
        blank=False,
    )

    # Admin panel configuration
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("campaign"),
                FieldPanel("campaign_page_type", read_only=True),
                FieldPanel("banner_image"),
                FieldPanel("name_ja"),
                FieldPanel("tagline"),
                FieldPanel("marketing_start_date", read_only=True),
                FieldPanel("start_date", read_only=True),
                FieldPanel("end_date", read_only=True),
            ],
            heading="Core Information",
        ),
        MultiFieldPanel(
            [
                FieldPanel("additional_details"),
            ],
            heading="Campaign Detail Information",
        ),
    ]

    # Api configuration
    api_fields = [
        APIField("campaign_page_type"),
        APIField("banner_image", serializer=HeaderImageFieldSerializer()),
        APIField("name_ja"),
        APIField("tagline"),
        APIField("marketing_start_date"),
        APIField("start_date"),
        APIField("end_date"),
        APIField("additional_details"),
    ]

    # Page limitations, Meta and methods
    parent_page_types = [
        "campaigns.CampaignListPage",
    ]

    def __str__(self) -> str:
        return self.title

    def clean(self):
        """Custom clean method to make start_date and end_date duplicate learning experience fields of same name. This denormalization and duplication is to reduce queries in the list views. Construct the slug string and replace auto generated slug with this string"""
        if not self.marketing_start_date == self.campaign.marketing_start_date:
            self.marketing_start_date = self.campaign.marketing_start_date
        if not self.start_date == self.campaign.start_date:
            self.start_date = self.campaign.start_date
        if not self.end_date == self.campaign.end_date:
            self.end_date = self.campaign.end_date

        # Make campaign model title and this display model title consistent
        if not self.title == self.campaign.name:
            self.title = self.campaign.name

        # Construct slug stringo
        slug = get_campaign_slug(self.title, self.start_date, self.end_date)
        if not self.slug == slug:
            self.slug = slug
