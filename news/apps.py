"""Configuration for the news application."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NewsConfig(AppConfig):
    """Application configuration for the news app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "news"
    verbose_name = _("News")
