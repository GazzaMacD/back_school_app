from django.contrib import admin

from .models import Tax


class TaxAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tax, TaxAdmin)
