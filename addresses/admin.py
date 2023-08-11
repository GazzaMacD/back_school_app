from django.contrib import admin

from .models import Address, ContactAddress


class ContactAddressInline(admin.TabularInline):
    model = ContactAddress
    extra = 0
    classes = ["collapse"]


class AddressAdmin(admin.ModelAdmin):
    model = Address


admin.site.register(Address, AddressAdmin)
