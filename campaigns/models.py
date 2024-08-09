from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

from core.models import TimeStampedModel

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
