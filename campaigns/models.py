from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.utils.text import slugify

from wagtail.api import APIField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Page
from wagtail_headless_preview.models import HeadlessMixin
from wagtail.fields import RichTextField

from core.models import TimeStampedModel


# Helpers
def get_campaign_slug(title, start_date, end_date):
    """Create campaign slug using title and dates"""
    start = f"{start_date:%Y-%m-%d}"
    end = f"{end_date:%Y-%m-%d}"
    return f"{slugify(title, allow_unicode=True)}-{start}-to-{end}"


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
    total_customer_increase = models.PositiveSmallIntegerField(
        _("Total Customer Increase"),
        blank=False,
        null=False,
        default=0,
        help_text="Required. Completed after campaign results finalized",
    )
    monthly_recurring_revenue_increase = models.DecimalField(
        _("Monthly Rec Rev Increase (￥)"),
        blank=False,
        null=False,
        max_digits=10,
        decimal_places=0,
        default=Decimal("0"),
        validators=[MinValueValidator(Decimal("0"))],
        help_text="Required. Completed after campaign results finalized in yen",
    )
    smart_goals_achieved = models.BooleanField(
        _("Smart Goals Achieved"),
        blank=False,
        null=False,
        default=False,
        help_text="Required. Completed after campaign results finalized. Please consider 'S' in SMART to answer this question",
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
