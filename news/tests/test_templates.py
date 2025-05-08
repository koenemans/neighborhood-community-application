from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from committees.models import Committee
from news.models import Post

class NewsTemplateTest(TestCase):
    def setUp(self):
        # Setup user and committee
        self.user = User.objects.create_user(username="testuser", email="user@example.com", password="password")
        self.group = Group.objects.create(name="Test Committee")
        self.committee = Committee.objects.create(
            group=self.group,
            slug="test-committee",
            description="A test committee",
            contact_person=self.user,
            email="test@example.com"
        )
        
        # Create test post
        self.post = Post.objects.create(
            title="Test Post Title",
            slug="test-post",
            content="Test content with <strong>HTML</strong>",
            committee=self.committee
        )
        
    def test_index_template_displays_posts(self):
        """Test that the index template displays posts correctly."""
        response = self.client.get(reverse('news:index'))
        self.assertContains(response, "Test Post Title")
        
    def test_detail_template_displays_post_content(self):
        """Test that the detail template displays post content correctly."""
        response = self.client.get(reverse('news:detail', kwargs={'slug': self.post.slug}))
        self.assertContains(response, "Test Post Title")
        self.assertContains(response, "Test content with &lt;strong&gt;HTML&lt;/strong&gt;") # Test content with <strong>HTML</strong>
        
    def test_archive_template_contains_filter_options(self):
        """Test that the archive template displays filter options."""
        response = self.client.get(reverse('news:archive'))
        self.assertContains(response, "Filter by Committee")
        self.assertContains(response, "Test Committee")  # Committee name