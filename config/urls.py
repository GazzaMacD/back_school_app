from django.conf import settings
from django.urls import include, path, re_path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from dj_rest_auth.views import PasswordResetConfirmView
from dj_rest_auth.registration.views import VerifyEmailView, ConfirmEmailView

from search import views as search_views
from .api import api_router

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = [
        path("__debug__/", include("debug_toolbar.urls")),
    ] + urlpatterns

# APi and Page Patterns
v2 = "api/v2"
urlpatterns = urlpatterns + [
    # API routes
    path(f"{v2}/contact/", include("contacts.urls")),
    path(f"{v2}/lesson-categories/", include("lessons.urls")),
    path(f"{v2}/auth/", include("dj_rest_auth.urls")),
    path(f"{v2}/auth/registration/", include("dj_rest_auth.registration.urls")),
    path(f"{v2}/", api_router.urls),
    # This path relates to the email that will be sent after requesting a password change
    # <django app base url>/api/v2/auth/password/reset/
    path(
        "password-reset-confirm/<str:uidb64>/<str:token>",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    # This path relates to the email that will be sent after registration
    re_path(
        r"confirm-email/(?P<key>[-:\w]+)",
        ConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
    # Should be last in list
    path("", include(wagtail_urls)),
]
