from django.test import TestCase
from django.conf import settings
from pathlib import Path
import os

class SettingsTest(TestCase):
    """Tests for the Django settings configuration."""
    
    def test_installed_apps(self):
        """Test that all required apps are installed."""
        self.assertIn('news.apps.NewsConfig', settings.INSTALLED_APPS)
        self.assertIn('activities.apps.ActivitiesConfig', settings.INSTALLED_APPS)
        self.assertIn('committees.apps.CommitteesConfig', settings.INSTALLED_APPS)
        self.assertIn('django.contrib.admin', settings.INSTALLED_APPS)
        self.assertIn('django.contrib.auth', settings.INSTALLED_APPS)
        self.assertIn('django.contrib.staticfiles', settings.INSTALLED_APPS)
        
    def test_middleware(self):
        """Test that all required middleware is installed."""
        self.assertIn('django.middleware.security.SecurityMiddleware', settings.MIDDLEWARE)
        self.assertIn('django.contrib.sessions.middleware.SessionMiddleware', settings.MIDDLEWARE)
        self.assertIn('django.middleware.csrf.CsrfViewMiddleware', settings.MIDDLEWARE)
        self.assertIn('django.contrib.auth.middleware.AuthenticationMiddleware', settings.MIDDLEWARE)
        
    def test_templates(self):
        """Test that templates are correctly configured."""
        templates_config = settings.TEMPLATES[0]
        self.assertEqual(templates_config['BACKEND'], 'django.template.backends.django.DjangoTemplates')
        self.assertIn(Path(settings.BASE_DIR) / 'templates', templates_config['DIRS'])
        self.assertTrue(templates_config['APP_DIRS'])
        
    def test_media_configuration(self):
        """Test that media settings are correctly configured."""
        self.assertEqual(settings.MEDIA_URL, '/media/')
        self.assertEqual(settings.MEDIA_ROOT, os.path.join(settings.BASE_DIR, 'media'))
