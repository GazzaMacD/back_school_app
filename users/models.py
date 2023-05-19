import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model with email instead of username along with
    other fields for names"""
    email = models.EmailField(
        _("email address"),
        unique=True,
        blank=False,
        null=False,
        help_text="*Required. Email must be unique for each user",
    )
    full_name = models.CharField(
        _("name"),
        blank=True,
        null=False,
        max_length=45,
        help_text="*Required. Full name in the name order user would like in public and in app.  Any character set is ok, 日本語 for example.",
    )
    full_en_name = models.CharField(
        _("english name"),
        blank=True,
        null=False,
        max_length=45,
        help_text="Full name in English, used for internal use. Not required but useful",
    )
    is_staff = models.BooleanField(
        _("is staff"),
        default=False,
        blank=False,
        null=False,
        help_text="*Required. Defines if user has access to the admin area of the site",
    )
    is_active = models.BooleanField(
        _("is active"),
        default=True,
        blank=False,
        null=False,
        help_text="*Required. Defines if user is active or not. Often better to set inactive rather than to delete a user",
    )
    date_joined = models.DateTimeField(
        _("date joined"),
        default=timezone.now,
        blank=False,
        null=False,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        abstract = False

    objects = CustomUserManager()

    def get_short_name(self):
        return self.email

    def natural_key(self):
        return self.email

    def __str__(self):
        return f"User: {self.full_name} Email:{self.email}"
