from wagtail.api.v2.views import PagesAPIViewSet
from django.contrib.contenttypes.models import ContentType
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet

# from wagtail_headless_preview.models import PagePreview
from rest_framework.response import Response

api_router = WagtailAPIRouter("wagtailapi")


# api_router.register_endpoint("page-preview", PagePreviewAPIViewSet)
api_router.register_endpoint("pages", PagesAPIViewSet)
api_router.register_endpoint("images", ImagesAPIViewSet)
api_router.register_endpoint("documents", DocumentsAPIViewSet)
