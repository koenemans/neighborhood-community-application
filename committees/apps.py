"""Configuration for the committees application."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CommitteesConfig(AppConfig):
    """Application configuration for the committees app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "committees"
    verbose_name = _("Committees")
