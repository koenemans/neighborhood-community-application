"""Configuration for the activities application."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ActivitiesConfig(AppConfig):
    """Application configuration for the activities app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "activities"
    verbose_name = _("Activities")
