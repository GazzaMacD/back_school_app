from django.contrib import admin

from .models import Contact, ContactEmail


class ContactEmailInline(admin.TabularInline):
    model = ContactEmail
    extra = 0


class ContactAdmin(admin.ModelAdmin):
    inlines = [
        ContactEmailInline,
    ]


admin.site.register(Contact, ContactAdmin)
