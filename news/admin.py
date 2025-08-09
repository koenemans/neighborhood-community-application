from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("title", "content")
    fieldsets = [
        (None, {"fields": ["title", "content", "committee"]}),
        (_("Image"), {"fields": ["poster"]}),
        (_("Attachment"), {"fields": ["attachment"]}),
        (_("Metadata"), {"fields": ["created_at"]}),
    ]


admin.site.register(Post, PostAdmin)
