from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from committees.models import Committee
from news.models import Post

class NewsAdminTest(TestCase):
    def setUp(self):
        # Create superuser
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password'
        )
        
        # Setup committee
        self.group = Group.objects.create(name="Test Committee")
        self.committee = Committee.objects.create(
            group=self.group,
            slug="test-committee",
            description="A test committee",
            contact_person=self.admin_user,
            email="test@example.com"
        )
        
        # Create test post
        self.post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            content="Test content",
            committee=self.committee
        )
        
        # Login admin
        self.client.login(username='admin', password='password')
        
    def test_post_listed_in_admin(self):
        """Test that posts are listed in the admin site."""
        response = self.client.get(reverse('admin:news_post_changelist'))
        self.assertContains(response, "Test Post")
        
    def test_post_admin_fields(self):
        """Test that the admin displays the correct fields for a post."""
        response = self.client.get(reverse('admin:news_post_change', args=[self.post.id]))
        self.assertContains(response, "Test Post")
        self.assertContains(response, "Test content")