from django.db import models


class SiteConfiguration(models.Model):
    """Stores customizable branding and contact details for the site."""

    site_name = models.CharField(max_length=255, default="Neighborhood Community")
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    logo = models.ImageField(upload_to="branding/", blank=True, null=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Site Configuration"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        if self.is_active:
            SiteConfiguration.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    @classmethod
    def get_active(cls):
        return cls.objects.filter(is_active=True).first() or cls.objects.first()
