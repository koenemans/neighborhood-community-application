from django.test import SimpleTestCase
from django.urls import reverse, resolve
from news.views import IndexView, DetailView, NewsArchiveView

class NewsURLsTest(SimpleTestCase):
    def test_index_url_resolves(self):
        """Test that the index URL resolves to the correct view."""
        url = reverse('news:index')
        self.assertEqual(resolve(url).func.view_class, IndexView)
    
    def test_detail_url_resolves(self):
        """Test that the detail URL resolves to the correct view and accepts a slug."""
        url = reverse('news:detail', kwargs={'slug': 'test-post'})
        self.assertEqual(resolve(url).func.view_class, DetailView)
        
    def test_archive_url_resolves(self):
        """Test that the archive URL resolves to the correct view."""
        url = reverse('news:archive')
        self.assertEqual(resolve(url).func.view_class, NewsArchiveView)