from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError

from .models import Contact, ContactEmail, Note
from addresses.admin import ContactAddressInline
from telnumbers.admin import TelNumberInline


class ContactEmailInlineFormSet(BaseInlineFormSet):
    count = 0

    def validate_unique(self) -> None:
        super().validate_unique()
        count = 0
        if len(self.forms):
            for form in self.forms:
                if form.instance.is_primary:
                    count += 1
            if count == 0 or count > 1:
                raise ValidationError(
                    [
                        {
                            "NON_FIELD_ERRORS": [
                                f"Currently there are {count} contact emails marked as primary! Contact emails must have {'only' if count > 1 else ''} 1 contact email marked as primary, please change your inputs."
                            ]
                        }
                    ]
                )


class ContactEmailInline(admin.TabularInline):
    model = ContactEmail
    extra = 0
    formset = ContactEmailInlineFormSet
    classes = ["collapse"]


class NoteInline(admin.TabularInline):
    model = Note
    extra = 0
    ordering = ["-created"]
    classes = ["collapse"]


class OrganizationInline(admin.TabularInline):
    model = Contact
    fk_name = "organization"
    can_delete = False
    extra = 0
    exclude = [
        "user",
        "ind_or_org",
    ]
    readonly_fields = [
        "name",
        "name_en",
        "status",
        "gender",
    ]
    verbose_name = "Organization Contacts"
    verbose_name_plural = "Organization Contacts"
    classes = ["collapse"]


class ContactAdmin(admin.ModelAdmin):
    list_display = ("name_en", "name", "user", "status", "organization")
    inlines = [
        ContactEmailInline,
        TelNumberInline,
        ContactAddressInline,
        NoteInline,
        OrganizationInline,
    ]


admin.site.register(Contact, ContactAdmin)
