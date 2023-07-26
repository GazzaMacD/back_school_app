from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel


class Contact(TimeStampedModel):
    name = models.CharField(
        _("name"),
        blank=True,
        null=False,
        max_length=100,
        help_text="Full name in the name order and language user would like. English or 日本語 for example. Max length: 100char",
    )
    name_en = models.CharField(
        _("english name"),
        blank=True,
        null=False,
        max_length=100,
        help_text="Full name in English, order should be same as name. Example 田中たろ should become Tanaka Taro in the field. Max length: 100char",
    )
