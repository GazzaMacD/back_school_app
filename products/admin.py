from django.contrib import admin

from .models import ProductService, ProductServicePrice, LearningExperience


class ProductServicePriceInline(admin.TabularInline):
    model = ProductServicePrice
    extra = 0


class LearningExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "start_date",
        "end_date",
        "max_people",
        "total_attended",
        "total_new",
        "total_profit",
    )


class ProductServiceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "service_or_product",
        "ptype",
        "price_summary",
        "tax_rate",
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
                    "tax_rate",
                    "price_summary",
                    "description",
                    ("min_num", "max_num"),
                    ("length", "length_unit"),
                    ("quantity", "quantity_unit"),
                    "is_native",
                    "is_online",
                    "is_inperson",
                    "has_onlinenotes",
                    "bookable_online",
                ],
            },
        ),
        (
            "Classes Information",
            {
                "fields": [
                    "class_type",
                ],
            },
        ),
    ]
    inlines = [
        ProductServicePriceInline,
    ]


admin.site.register(ProductService, ProductServiceAdmin)
admin.site.register(LearningExperience, LearningExperienceAdmin)
