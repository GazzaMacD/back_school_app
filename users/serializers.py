from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import Group
from django.urls import exceptions as url_exceptions
from django.utils.translation import gettext_lazy as _
from dj_rest_auth.serializers import UserDetailsSerializer, PasswordResetSerializer
from rest_framework import serializers
from rest_framework import exceptions, serializers

from contacts.serializers import ContactUserSerializer
from .models import CustomUser

# Get the UserModel
UserModel = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name",)


class CustomUserDetailsSerializer(UserDetailsSerializer):
    groups = GroupSerializer(many=True)
    contact = ContactUserSerializer()

    class Meta(UserDetailsSerializer.Meta):
        fields = (
            "email",
            "contact",
            "is_staff",
            "groups",
        )


class CustomUserContactNameSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="contact.name")

    class Meta:
        model = CustomUser
        fields = ("name",)


class CustomLoginSerializer(serializers.Serializer):
    """Login serializer from dj-rest-auth==4.0.1. Japanese validation messages"""

    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(
        required=False,
        allow_blank=True,
        error_messages={
            "invalid": "有効なEメールアドレスを入力してください",
        },
    )
    password = serializers.CharField(
        style={"input_type": "password"},
        error_messages={
            "blank": "パスワードを入力してください",
        },
    )

    def authenticate(self, **kwargs):
        return authenticate(self.context["request"], **kwargs)

    def _validate_email(self, email, password):
        if email and password:
            user = self.authenticate(email=email, password=password)
        else:
            msg = _("「Eメール」と「パスワード」の両方が必要です")
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username(self, username, password):
        if username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = _('Must include "username" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username_email(self, username, email, password):
        if email and password:
            user = self.authenticate(email=email, password=password)
        elif username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = _('Must include either "username" or "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def get_auth_user_using_allauth(self, username, email, password):
        from allauth.account import app_settings as allauth_account_settings

        # Authentication through email
        if (
            allauth_account_settings.AUTHENTICATION_METHOD
            == allauth_account_settings.AuthenticationMethod.EMAIL
        ):
            return self._validate_email(email, password)

        # Authentication through username
        if (
            allauth_account_settings.AUTHENTICATION_METHOD
            == allauth_account_settings.AuthenticationMethod.USERNAME
        ):
            return self._validate_username(username, password)

        # Authentication through either username or email
        return self._validate_username_email(username, email, password)

    def get_auth_user_using_orm(self, username, email, password):
        if email:
            try:
                username = UserModel.objects.get(email__iexact=email).get_username()
            except UserModel.DoesNotExist:
                pass

        if username:
            return self._validate_username_email(username, "", password)

        return None

    def get_auth_user(self, username, email, password):
        """
        Retrieve the auth user from given POST payload by using
        either `allauth` auth scheme or bare Django auth scheme.

        Returns the authenticated user instance if credentials are correct,
        else `None` will be returned
        """
        if "allauth" in settings.INSTALLED_APPS:
            # When `is_active` of a user is set to False, allauth tries to return template html
            # which does not exist. This is the solution for it. See issue #264.
            try:
                return self.get_auth_user_using_allauth(username, email, password)
            except url_exceptions.NoReverseMatch:
                msg = _("提供された認証情報ではログインできません")
                raise exceptions.ValidationError(msg)
        return self.get_auth_user_using_orm(username, email, password)

    @staticmethod
    def validate_auth_user_status(user):
        if not user.is_active:
            msg = _("ユーザーアカウントが無効になっている")
            raise exceptions.ValidationError(msg)

    @staticmethod
    def validate_email_verification_status(user, email=None):
        from allauth.account import app_settings as allauth_account_settings

        if (
            allauth_account_settings.EMAIL_VERIFICATION
            == allauth_account_settings.EmailVerificationMethod.MANDATORY
            and not user.emailaddress_set.filter(
                email=user.email, verified=True
            ).exists()
        ):
            raise serializers.ValidationError(_("Eメールが認証されていない"))

    def validate(self, attrs):
        username = attrs.get("username")
        email = attrs.get("email")
        password = attrs.get("password")
        user = self.get_auth_user(username, email, password)

        if not user:
            msg = _("提供された認証情報ではログインできません")
            raise exceptions.ValidationError(msg)

        # Did we get back an active user?
        self.validate_auth_user_status(user)

        # If required, is the email verified?
        if "dj_rest_auth.registration" in settings.INSTALLED_APPS:
            self.validate_email_verification_status(user, email=email)

        attrs["user"] = user
        return attrs


class CustomPasswordResetSerializer(PasswordResetSerializer):
    """
    Custom serializer for requesting a password reset e-mail with
    japanese error messages.
    """

    email = serializers.EmailField(
        error_messages={
            "invalid": "有効なEメールアドレスを入力してください",
            "blank": "Eメールアドレスを入力してください",
            "required": "Eメールアドレスを入力してください",
        },
    )
