from django.contrib import admin

from .models import Campaign


class CampaignAdmin(admin.ModelAdmin):
    ordering = ("-start_date",)
    search_fields = ("name",)
    list_display = (
        "name",
        "start_date",
        "end_date",
        "total_customer_increase",
        "monthly_recurring_revenue_increase",
        "smart_goals_achieved",
    )


admin.site.register(Campaign, CampaignAdmin)
