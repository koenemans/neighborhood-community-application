from .models import SiteConfiguration


def site_settings(request):
    """Add site configuration to context."""
    return {"site_config": SiteConfiguration.objects.first()}
