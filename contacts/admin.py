from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError

from .models import Contact, ContactEmail, Note
from addresses.admin import ContactAddressInline


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


class ContactAdmin(admin.ModelAdmin):
    inlines = [
        ContactEmailInline,
        ContactAddressInline,
        NoteInline,
    ]


admin.site.register(Contact, ContactAdmin)
