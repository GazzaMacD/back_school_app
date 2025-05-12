from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel


class VideoCall(TimeStampedModel):
    teacher = models.OneToOneField(
        "users.CustomUser",
        on_delete=models.CASCADE,
        limit_choices_to={"is_staff": True},
        blank=False,
        related_name="videocall",
        help_text=_(
            "Required. Please choose the teacher who this video call room will be for."
        ),
    )
    host_room_url = models.URLField(
        null=False,
        blank=False,
        max_length=1000,
        help_text=_(
            "Required. Please add the HOST url for the teacher here. Max length 1000char"
        ),
    )
    room_url = models.URLField(
        null=False,
        blank=False,
        max_length=500,
        help_text=_(
            "Required. Please add the ROOM url for the teacher here. Max length 500char"
        ),
    )
    slug = models.SlugField(
        null=False,
        blank=False,
        unique=True,
        editable=False,
        max_length=200,
    )

    def __str__(self):
        return f"{self.teacher.contact.name_en} video call"

    def _get_unique_slug(self):
        slug = slugify(f"{self.teacher.contact.name_en}")
        unique_slug = slug

        if not VideoCall.objects.filter(slug=unique_slug).exists():
            return unique_slug
        else:
            if VideoCall.objects.filter(slug=unique_slug)[0].id == self.id:
                return unique_slug
            # create unique slug
            else:
                counter = 1
                while VideoCall.objects.filter(slug=unique_slug).exists():
                    unique_slug = f"{slug}-{counter}"
                    counter += 1
                return unique_slug

    def clean(self):
        self.slug = self._get_unique_slug()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
