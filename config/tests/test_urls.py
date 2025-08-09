from django.test import TestCase, Client
from django.urls import reverse, resolve
from news.views import HomePageView, IndexView as NewsIndexView
from activities.views import IndexView as ActivitiesIndexView
from committees.views import IndexView as CommitteesIndexView


class URLConfigTest(TestCase):
    """Tests for the main URL configuration."""
    
    def setUp(self):
        self.client = Client()
        
    def test_home_url_resolves(self):
        """Test that the home URL resolves to the correct view."""
        url = reverse('home')
        self.assertEqual(url, '/')
        self.assertEqual(resolve(url).func.view_class, HomePageView)
        
    def test_news_urls_resolve(self):
        """Test that the news URLs resolve correctly."""
        # News index
        url = reverse('news:index')
        self.assertEqual(url, '/news/')
        self.assertEqual(resolve(url).func.view_class, NewsIndexView)
        
        # News archive
        url = reverse('news:archive')
        self.assertEqual(url, '/news/archive/')
        
    def test_activities_urls_resolve(self):
        """Test that the activities URLs resolve correctly."""
        # Activities index
        url = reverse('activities:index')
        self.assertEqual(url, '/activities/')
        self.assertEqual(resolve(url).func.view_class, ActivitiesIndexView)
        
        # Activities archive
        url = reverse('activities:archive')
        self.assertEqual(url, '/activities/archive/')
        
    def test_committees_urls_resolve(self):
        """Test that the committees URLs resolve correctly."""
        # Committees index
        url = reverse('committees:index')
        self.assertEqual(url, '/committees/')
        self.assertEqual(resolve(url).func.view_class, CommitteesIndexView)
        
    def test_admin_url_resolves(self):
        """Test that the admin URL resolves correctly."""
        url = reverse('admin:index')
        self.assertEqual(url, '/admin/')
        
    def test_homepage_status_code(self):
        """Test that the homepage returns a 200 status code."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
