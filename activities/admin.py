"""Admin configuration for the activities application."""

from django.contrib import admin
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

    def has_change_permission(self, request, obj=None):
        """Restrict edits to activities belonging to the user's committees."""
        has_perm = super().has_change_permission(request, obj)
        if not has_perm:
            return False
        if obj is not None and not request.user.is_superuser:
            return obj.committee.group in request.user.groups.all()
        return True

    def has_delete_permission(self, request, obj=None):
        """Restrict deletions to activities belonging to the user's committees."""
        has_perm = super().has_delete_permission(request, obj)
        if not has_perm:
            return False
        if obj is not None and not request.user.is_superuser:
            return obj.committee.group in request.user.groups.all()
        return True

    def has_view_permission(self, request, obj=None):
        """Restrict viewing to activities belonging to the user's committees."""
        has_perm = super().has_view_permission(request, obj)
        if not has_perm:
            return False
        if obj is not None and not request.user.is_superuser:
            return obj.committee.group in request.user.groups.all()
        return True


admin.site.register(Activity, ActivityAdmin)
