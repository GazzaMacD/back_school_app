import re

from django.contrib.auth.password_validation import (
    UserAttributeSimilarityValidator,
    MinimumLengthValidator,
    NumericPasswordValidator,
    CommonPasswordValidator,
    exceeds_maximum_length_ratio,
)
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError, FieldDoesNotExist
from difflib import SequenceMatcher


class CustomUserAttributeSimilarityValidator(UserAttributeSimilarityValidator):
    def validate(self, password, user=None):
        if not user:
            return

        password = password.lower()
        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_lower = value.lower()
            value_parts = re.split(r"\W+", value_lower) + [value_lower]
            for value_part in value_parts:
                if exceeds_maximum_length_ratio(
                    password, self.max_similarity, value_part
                ):
                    continue
                if (
                    SequenceMatcher(a=password, b=value_part).quick_ratio()
                    >= self.max_similarity
                ):
                    try:
                        verbose_name = str(
                            user._meta.get_field(attribute_name).verbose_name
                        )
                    except FieldDoesNotExist:
                        verbose_name = attribute_name
                    raise ValidationError(
                        _("パスワードが %(verbose_name)s のものと似すぎている"),
                        code="password_too_similar",
                        params={"verbose_name": verbose_name},
                    )

    def get_help_text(self):
        return _("パスワードは、お客様の個人情報に類似したものを避けてください")


class CustomMinimumLengthValidator(MinimumLengthValidator):
    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _(f"{self.min_length}桁以上のパスワードを登録してください"),
                code="password_too_short",
                params={"min_length": self.min_length},
            )

    def get_help_text(self):
        return _(f"{self.min_length}桁以上のパスワードを登録してください")


class CustomNumericPasswordValidator(NumericPasswordValidator):
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                _("パスワードは, 全て数字のを避けてください"),
                code="password_entirely_numeric",
            )

    def get_help_text(self):
        return _("パスワードは, 全て数字のを避けてください")


class CustomCommonPasswordValidator(CommonPasswordValidator):
    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                _("よく利用されているパスワードのご登録を避けてください"),
                code="password_too_common",
            )

    def get_help_text(self):
        return _("よく利用されているパスワードのご登録を避けてください")
