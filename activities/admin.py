"""Admin configuration for the activities application."""

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Activity


class ActivityAdmin(admin.ModelAdmin):
    """Admin interface definition for :class:`~activities.models.Activity`."""

    list_display = ("title", "location", "start", "end")
    list_filter = ("start", "end")
    search_fields = ("title", "content", "location")
    fieldsets = [
        (None, {"fields": ["title", "content", "committee"]}),
        (_("Practical Information"), {"fields": ["location", "start", "end"]}),
        (_("Image"), {"fields": ["poster"]}),
        (_("Metadata"), {"fields": ["created_at"]}),
    ]

    def clean(self):
        """Validate that the end date is not before the start date."""
        cleaned_data = super().clean()
        start = cleaned_data.get("start")
        end = cleaned_data.get("end")
        if start and end:
            if end < start:
                raise ValidationError(
                    _("End date %(end)s cannot be before the start date %(start)s")
                    % {"end": end, "start": start},
                    code="invalid",
                )
        return cleaned_data


admin.site.register(Activity, ActivityAdmin)
