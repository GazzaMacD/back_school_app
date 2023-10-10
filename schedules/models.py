from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from core.models import TimeStampedModel


class SuperSassSchedule(TimeStampedModel):
    teacher = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        limit_choices_to={"is_staff": True},
        blank=False,
        related_name="super_sass_schedules",
        help_text=_("Required. Please choose the teacher who this schedule is for."),
    )
    language_school = models.ForeignKey(
        "languageschools.LanguageSchool",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="language_schools",
        help_text=_(
            "Required. Please choose the language school this schedule is for."
        ),
    )
    slug = models.SlugField(
        null=False,
        blank=False,
        unique=True,
        editable=False,
        max_length=100,
    )
    schedule_url = models.URLField(
        null=False,
        blank=False,
        max_length=300,
        help_text=_(
            "Required. Please add the url for the teacher here .Please check name and ls are correct."
        ),
    )

    def __str__(self):
        return f"{self.teacher.contact.name_en} {self.language_school.name} schedule"

    def _get_unique_slug(self):
        slug = slugify(f"{self.teacher.contact.name_en} {self.language_school.name}")
        unique_slug = slug

        if not SuperSassSchedule.objects.filter(slug=unique_slug).exists():
            return unique_slug
        else:
            if SuperSassSchedule.objects.filter(slug=unique_slug)[0].id == self.id:
                return unique_slug
            # create unique slug
            else:
                counter = 1
                while SuperSassSchedule.objects.filter(slug=unique_slug).exists():
                    unique_slug = f"{slug}-{counter}"
                    counter += 1
                return unique_slug

    def clean(self):
        self.slug = self._get_unique_slug()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
