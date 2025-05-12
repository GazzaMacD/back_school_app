from django.contrib import admin

from .models import VideoCall


class VideoCallAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Video Calls creation times and slug",
            {
                "fields": (
                    ("created", "modified"),
                    "slug",
                ),
            },
        ),
        (
            "Details for Video Calls",
            {
                "fields": (
                    "teacher",
                    "host_room_url",
                    "room_url",
                ),
            },
        ),
    )
    readonly_fields = ("created", "modified", "slug")


admin.site.register(VideoCall, VideoCallAdmin)
