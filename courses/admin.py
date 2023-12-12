from django.contrib import admin

from .models import Course


class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "title_en",
        "subject",
        "course_category",
    )


admin.site.register(Course, CourseAdmin)
