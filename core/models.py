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


class SubjectChoices(models.TextChoices):
    """Text choices fields for all subjects. Currently using comma split values so as to
    speed up queries rather than using a foreign key relation to subject model. May change in future. First value is roughly based on ISO 639-1 codes. May develop own code system if subjects go beyond language.
    """

    ENGLISH = "english", "en,English,英語"
    JAPANESE = "japanese", "ja,Japanese,日本語"
    FRENCH = "french", "fr,French,フランス語"


class LevelChoices(models.IntegerChoices):
    """Integer choices for all levels of various courses"""

    NONE = 0, "None,ない"
    ALL = 1, "All,全級"
    ELEMENTARY = 2, "Elementary,初級"
    LOWER_INTERMEDIATE = 3, "Lower Intermediate, 中初級"
    INTERMEDIATE = 4, "Intermediate,中級 "
    UPPER_INTERMEDIATE = 5, "Upper Intermediate,中上級"
    ADVANCED = 6, "Advanced,上級"
    GRADE_1 = 7, "Grade 1,1級"
    GRADE_PRE1 = 8, "Grade Pre-1,準1級"
    GRADE_2 = 9, "Grade 2,2級"
    GRADE_PRE2 = 10, "Grade Pre-2,準2級"
    GRADE_3 = 11, "Grade 3,3級"
    GRADE_4 = 12, "Grade 4,4級"
    GRADE_5 = 13, "Grade 5,5級"


class CourseCategoryChoices(models.TextChoices):
    """Text choices for categories of courses"""

    GENERAL = "general", "General,日常"
    BUSINESS = "business", "Business,ビジネス"
    TEST_PREPARATION = "testpreparation", "Test Preparation,テスト対策"
    WRITING = "writing", "Writing,ライティング"
