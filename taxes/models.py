from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel


class TaxTypeChoices(models.TextChoices):
    CONSUMPTION = "CN", _("Consumption,消費税")


class Tax(TimeStampedModel):
    """Model to hold all taxes for the application"""

    name = models.CharField(
        _("Name"),
        null=False,
        blank=False,
        unique=True,
        max_length=100,
        help_text=_(
            "Required. Max length 100. Must be a unique identifying name in English for this tax"
        ),
    )
    tax_type = models.CharField(
        _("Tax Type"),
        null=False,
        blank=False,
        default=TaxTypeChoices.CONSUMPTION,
        choices=TaxTypeChoices.choices,
        help_text="Required",
    )
    rate = models.DecimalField(
        _("Tax rate"),
        null=False,
        blank=False,
        max_digits=10,
        decimal_places=2,
        help_text=_("Required. Max digits 5. Max decimal places 2."),
    )
    start_date = models.DateTimeField(
        _("Start date"),
        blank=False,
        null=False,
        help_text="Required. Please make sure to set when this rate became officially applicable. It is generally never changed",
    )
    end_date = models.DateTimeField(
        _("End date"),
        blank=True,
        null=True,
        help_text="Not Required. **IMPORTANT. Do not set this until the tax is officially declared null and void. Make sure to change all products or other tables that use this rate before setting this. Thankyou.",
    )

    def __str__(self):
        return f"{self.name} ({self.rate}%)"

    class Meta:
        verbose_name_plural = "Taxes"
