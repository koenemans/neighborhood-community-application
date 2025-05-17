from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class CommitteesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'committees'
    verbose_name = _('Committees')
