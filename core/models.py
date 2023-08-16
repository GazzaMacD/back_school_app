from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    created and modified fields
    """

    created = models.DateTimeField(
        _("created"),
        auto_now_add=True,
    )
    modified = models.DateTimeField(
        _("modified"),
        auto_now=True,
    )

    class Meta:
        abstract = True


@register_snippet
class Language(models.Model):
    """Model to hold languages for various uses in the site"""

    # Fields
    name_en = models.CharField(
        "English name",
        blank=False,
        null=False,
        max_length=40,
        help_text="Required. Max length 40 chars",
    )
    name_ja = models.CharField(
        "Japanese Name",
        blank=False,
        null=False,
        max_length=40,
        help_text="Required. Max length 40 chars",
    )
    slug = models.CharField(
        "Slug",
        unique=True,
        blank=False,
        null=False,
        max_length=50,
        help_text="Required. Use English name to create a slug with only hypens and lowercase letters",
    )

    # Panels
    panels = [
        FieldPanel("name_en"),
        FieldPanel("name_ja"),
        FieldPanel("slug"),
    ]

    def __str__(self):
        return self.name_en

    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"
