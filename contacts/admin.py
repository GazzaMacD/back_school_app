from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError

from .models import Contact, ContactEmail


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


class ContactAdmin(admin.ModelAdmin):
    inlines = [
        ContactEmailInline,
    ]


admin.site.register(Contact, ContactAdmin)
