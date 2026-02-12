from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from siteconfig.models import SiteConfiguration


class SettingsViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="admin", password="password", is_staff=True
        )

    def test_anonymous_user_redirected(self):
        response = self.client.get(reverse("siteconfig:settings"))
        self.assertEqual(response.status_code, 302)

    def test_staff_user_can_update_configuration(self):
        self.client.login(username="admin", password="password")
        response = self.client.post(
            reverse("siteconfig:settings"),
            {
                "site_name": "My New Site",
                "contact_email": "test@example.com",
                "contact_phone": "1234567890",
            },
        )
        self.assertRedirects(response, reverse("siteconfig:settings"))
        config = SiteConfiguration.get_active()
        self.assertEqual(config.site_name, "My New Site")
        self.assertEqual(config.contact_email, "test@example.com")
        self.assertEqual(config.contact_phone, "1234567890")
