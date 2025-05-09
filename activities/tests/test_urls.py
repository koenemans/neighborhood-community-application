from django.test import SimpleTestCase
from django.urls import reverse, resolve
from activities.views import IndexView, DetailView, ActivitiesArchiveView

class ActivitiesURLsTest(SimpleTestCase):
    def test_index_url_resolves(self):
        """Test that the index URL resolves to the correct view."""
        url = reverse('activities:index')
        self.assertEqual(resolve(url).func.view_class, IndexView)
    
    def test_detail_url_resolves(self):
        """Test that the detail URL resolves to the correct view and accepts a slug."""
        url = reverse('activities:detail', kwargs={'slug': 'test-activity'})
        self.assertEqual(resolve(url).func.view_class, DetailView)
        
    def test_archive_url_resolves(self):
        """Test that the archive URL resolves to the correct view."""
        url = reverse('activities:archive')
        self.assertEqual(resolve(url).func.view_class, ActivitiesArchiveView)