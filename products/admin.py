from django.contrib import admin

from .models import ProductService


class ProductServiceAdmin(admin.ModelAdmin):
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
                    "service_or_product",
                    "ptype",
                ],
            },
        ),
    ]


admin.site.register(ProductService, ProductServiceAdmin)
