from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "id",
    )
    readonly_fields = [
        "slug",
        "created",
        "modified",
    ]
    fieldsets = [
        (
            "Product Basic Information",
            {
                "fields": [
                    "name",
                    "slug",
                    "created",
                    "modified",
                ],
            },
        ),
    ]


admin.site.register(Product, ProductAdmin)
