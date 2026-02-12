from django.test import TestCase
from django.urls import reverse
from django.test import override_settings
from siteconfig.models import SiteConfiguration


@override_settings(LANGUAGE_CODE="en-us")
class TemplateTest(TestCase):
    """Tests for template loading and rendering."""

    def test_base_template_elements(self):
        """Test that the base template loads and contains necessary elements."""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

        # Check for basic structure
        self.assertContains(response, "<html")
        self.assertContains(response, "<head")
        self.assertContains(response, "<body")
        self.assertContains(response, "<header")
        self.assertContains(response, "<main")
        self.assertContains(response, "<footer")

        # Check for navigation elements
        self.assertContains(response, "News</a>")
        self.assertContains(response, "Activities</a>")
        self.assertContains(response, "Committees</a>")

        # Check for copyright in footer
        self.assertContains(response, "Neighborhood Community")

    def test_custom_site_name_displayed(self):
        SiteConfiguration.objects.create(site_name="Custom Name")
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Custom Name")

    def test_responsive_meta_tag(self):
        """Test that the viewport meta tag is included for responsiveness."""
        response = self.client.get(reverse("home"))
        self.assertContains(
            response,
            '<meta name="viewport" content="width=device-width, initial-scale=1.0',
        )
