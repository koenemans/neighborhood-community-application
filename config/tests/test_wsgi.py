from django.test import TestCase
import os
import importlib.util
from config.wsgi import application

class WSGITest(TestCase):
    """Tests for the WSGI configuration."""
    
    def test_wsgi_application_loads(self):
        """Test that the WSGI application can be loaded."""
        self.assertIsNotNone(application)
        
    def test_wsgi_env_variable(self):
        """Test that the DJANGO_SETTINGS_MODULE environment variable is set."""
        self.assertEqual(os.environ.get('DJANGO_SETTINGS_MODULE'), 'config.settings')
