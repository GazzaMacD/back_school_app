from django.db import models

from wagtail.models import Page


class HomePage(Page):
    pass

    # Page limitations
    max_count = 1
    parent_page_types = ["wagtailcore.Page"]
    # subpage_types = ["blog.BlogIndexPage"]
