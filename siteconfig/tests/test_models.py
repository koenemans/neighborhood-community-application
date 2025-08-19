from django.test import TestCase
from siteconfig.models import SiteConfiguration


class SiteConfigurationModelTests(TestCase):
    def test_only_one_active_configuration(self):
        config1 = SiteConfiguration.objects.create(site_name="First", is_active=True)
        config2 = SiteConfiguration.objects.create(site_name="Second", is_active=True)
        config1.refresh_from_db()
        config2.refresh_from_db()
        self.assertFalse(config1.is_active)
        self.assertTrue(config2.is_active)

    def test_get_active_switches(self):
        config1 = SiteConfiguration.objects.create(site_name="First", is_active=True)
        config2 = SiteConfiguration.objects.create(site_name="Second")
        self.assertEqual(SiteConfiguration.get_active(), config1)
        config2.is_active = True
        config2.save()
        self.assertEqual(SiteConfiguration.get_active(), config2)
