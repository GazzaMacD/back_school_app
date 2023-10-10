from django.contrib import admin

from .models import SuperSassSchedule


class SuperSassScheduleAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Individual Schedule status, creation times and slug",
            {
                "fields": (
                    ("created", "modified"),
                    "slug",
                ),
            },
        ),
        (
            "Details for Schedule",
            {
                "fields": (
                    "teacher",
                    "language_school",
                    "schedule_url",
                ),
            },
        ),
    )
    readonly_fields = ("created", "modified", "slug")


admin.site.register(SuperSassSchedule, SuperSassScheduleAdmin)
