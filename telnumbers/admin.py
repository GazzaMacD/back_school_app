from django.contrib import admin

from .models import TelNumber


class TelNumberInline(admin.TabularInline):
    model = TelNumber
    extra = 0
    classes = ["collapse"]
