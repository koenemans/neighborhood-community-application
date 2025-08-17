from django import forms
from .models import SiteConfiguration


class SiteConfigurationForm(forms.ModelForm):
    class Meta:
        model = SiteConfiguration
        fields = ["site_name", "contact_email", "contact_phone", "logo"]
