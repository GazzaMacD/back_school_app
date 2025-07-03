from functools import lru_cache

from django.contrib import admin

from .models import Campaign


class CampaignAdmin(admin.ModelAdmin):
    ordering = ("-start_date",)
    search_fields = ("name",)
    fieldsets = [
        (
            "Campaign Basic Information",
            {
                "fields": [
                    "name",
                    "marketing_start_date",
                    "start_date",
                    "end_date",
                    "description",
                ],
            },
        ),
        (
            "Campaign Data",
            {
                "fields": [
                    "target_total_customer_increase",
                    "total_customer_increase",
                    "target_monthly_recurring_revenue_increase",
                    "monthly_recurring_revenue_increase",
                    "smart_goals_achieved",
                ],
            },
        ),
        (
            "Campaign Note",
            {
                "fields": [
                    "note",
                ],
            },
        ),
    ]
    list_display = (
        "name",
        "marketing_start_date",
        "start_date",
        "end_date",
        "target_monthly_recurring_revenue_increase",
        "monthly_recurring_revenue_increase",
        "actual_vs_target_rev_increase",
        "smart_goals_achieved",
    )

    @lru_cache
    def actual_vs_target_rev_increase(self, obj):
        return (
            obj.monthly_recurring_revenue_increase
            - obj.target_monthly_recurring_revenue_increase
        )


admin.site.register(Campaign, CampaignAdmin)
