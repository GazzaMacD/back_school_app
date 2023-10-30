from django.contrib import admin

from .models import ProductService, ProductServicePrice, LearningExperience


class ProductServicePriceInline(admin.TabularInline):
    model = ProductServicePrice
    extra = 0


class LearningExperienceAdmin(admin.ModelAdmin):
    list_display = ("name",)


class ProductServiceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "service_or_product",
        "ptype",
        "price_summary",
        "id",
    )
    readonly_fields = [
        "slug",
        "created",
        "modified",
        "price_summary",
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
                    "price_summary",
                    "description",
                ],
            },
        ),
    ]
    inlines = [
        ProductServicePriceInline,
    ]


admin.site.register(ProductService, ProductServiceAdmin)
admin.site.register(LearningExperience, LearningExperienceAdmin)
