from django.contrib import admin
from .models import SiteConfiguration


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ("site_name", "contact_email", "contact_phone", "is_active")
    list_editable = ("is_active",)
