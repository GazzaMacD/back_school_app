from django.contrib import admin

from .models import LearningCenter


class LearningCenterAdmin(admin.ModelAdmin):
    pass


admin.site.register(LearningCenter, LearningCenterAdmin)
