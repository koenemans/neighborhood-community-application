from django.test import SimpleTestCase
from django.urls import reverse, resolve
from committees.views import IndexView, DetailView

class CommitteesURLsTest(SimpleTestCase):
    def test_index_url_resolves(self):
        """Test that the index URL resolves to the correct view."""
        url = reverse('committees:index')
        self.assertEqual(resolve(url).func.view_class, IndexView)
    
    def test_detail_url_resolves(self):
        """Test that the detail URL resolves to the correct view and accepts a slug."""
        url = reverse('committees:detail', kwargs={'slug': 'test-committee'})
        self.assertEqual(resolve(url).func.view_class, DetailView)
