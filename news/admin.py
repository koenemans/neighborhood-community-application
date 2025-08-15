"""Admin configuration for the news application."""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Post


class PostAdmin(admin.ModelAdmin):
    """Admin interface definition for :class:`~news.models.Post`."""

    list_display = ("title", "created_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("title", "content")
    fieldsets = [
        (None, {"fields": ["title", "content", "committee"]}),
        (_("Image"), {"fields": ["poster"]}),
        (_("Attachment"), {"fields": ["attachment"]}),
        (_("Metadata"), {"fields": ["created_at"]}),
    ]

    def has_change_permission(self, request, obj=None):
        """Restrict edits to posts belonging to the user's committees."""
        has_perm = super().has_change_permission(request, obj)
        if not has_perm:
            return False
        if obj is not None and not request.user.is_superuser:
            return obj.committee.group in request.user.groups.all()
        return True

    def has_delete_permission(self, request, obj=None):
        """Restrict deletions to posts belonging to the user's committees."""
        has_perm = super().has_delete_permission(request, obj)
        if not has_perm:
            return False
        if obj is not None and not request.user.is_superuser:
            return obj.committee.group in request.user.groups.all()
        return True

    def has_view_permission(self, request, obj=None):
        """Restrict viewing to posts belonging to the user's committees."""
        has_perm = super().has_view_permission(request, obj)
        if not has_perm:
            return False
        if obj is not None and not request.user.is_superuser:
            return obj.committee.group in request.user.groups.all()
        return True


admin.site.register(Post, PostAdmin)
