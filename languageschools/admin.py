from django.contrib import admin

from .models import LanguageSchool


class LanguageSchoolAdmin(admin.ModelAdmin):
    pass


admin.site.register(LanguageSchool, LanguageSchoolAdmin)
