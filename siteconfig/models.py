from django.db import models


class SiteConfiguration(models.Model):
    """Stores customizable branding and contact details for the site."""

    site_name = models.CharField(max_length=255, default="Neighborhood Community")
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    logo = models.ImageField(upload_to="branding/", blank=True, null=True)

    class Meta:
        verbose_name = "Site Configuration"

    def __str__(self):
        return self.site_name
