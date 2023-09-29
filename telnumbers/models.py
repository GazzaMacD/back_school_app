from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel


class TelNumberChoices(models.TextChoices):
    HOME_FIXED = "HOF", _("Fixed Home Phone")
    WORK_FIXED = "WOF", _("Fixed Work Phone")
    PERSONAL_MOBILE = "PEM", _("Personal mobile")
    WORK_MOBILE = "WOM", _("Work Mobile")


class TelNumber(TimeStampedModel):
    contact = models.ForeignKey(
        "contacts.Contact",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    identifier = models.CharField(
        _("Easy Identifier"),
        null=False,
        blank=True,
        max_length=150,
        help_text=_("Not required, max 150 char"),
    )
    number = models.CharField(
        _("Telephone Number"),
        null=False,
        blank=False,
        max_length=15,
        help_text=_("Required, max 15 char"),
    )
    number_type = models.CharField(
        _("Type"),
        null=False,
        blank=False,
        max_length=3,
        choices=TelNumberChoices.choices,
        default=TelNumberChoices.PERSONAL_MOBILE,
        help_text=_("Required"),
    )
    is_primary = models.BooleanField(
        _("Is primary"),
        blank=False,
        null=False,
        default=False,
        help_text=_("Required. Should be only one per place or contact"),
    )
    is_learning_center = models.BooleanField(
        _("Is Learning Center"),
        null=False,
        blank=False,
        default=False,
    )

    def __str__(self) -> str:
        if self.identifier:
            return f"{self.identifier} - {self.number}"
        return self.number
