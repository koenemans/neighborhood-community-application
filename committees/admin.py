"""Admin configuration for the committees application."""

from django.contrib import admin

from .models import Committee


class CommitteeAdmin(admin.ModelAdmin):
    """Admin interface definition for :class:`~committees.models.Committee`."""

    list_display = ("group", "email", "contact_person")
    search_fields = ("group", "email", "contact_person")
    fieldsets = [
        (None, {"fields": ["group", "email", "contact_person", "description"]}),
    ]


admin.site.register(Committee, CommitteeAdmin)
