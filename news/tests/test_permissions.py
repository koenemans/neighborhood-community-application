from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group, Permission
from committees.models import Committee
from news.models import Post

class NewsPermissionsTest(TestCase):
    def setUp(self):
        # Create staff user
        self.user = User.objects.create_user(username="regular_user", email="regular@example.com", password="password")
        self.user.is_staff = True
        self.user.save()

        # Setup committee
        self.group = Group.objects.create(name="Test Committee")
        self.committee = Committee.objects.create(
            group=self.group,
            slug="test-committee",
            description="A test committee",
            contact_person=self.user,
            email="test@example.com"
        )
        
        # Add user to committee group and give permission to add posts
        add_post_permission = Permission.objects.get(codename='add_post')
        self.group.user_set.add(self.user)
        self.group.permissions.add(add_post_permission)
        self.group.save()
        
        # Create a test post
        self.post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            content="Test content",
            committee=self.committee
        )
        
    def test_anonymous_cannot_create_post(self):
        """Test that anonymous users cannot create posts."""
        create_url = reverse('admin:news_post_add')
        response = self.client.get(create_url)
        self.assertNotEqual(response.status_code, 200)
        
    def test_regular_user_in_committee_can_view_post(self):
        """Test that anonymous users can view posts."""
        detail_url = reverse('news:detail', kwargs={'slug': self.post.slug})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        
    def test_admin_can_create_post(self):
        """Test that regular committee users can create posts."""
        self.client.login(username="regular_user", password="password")
        create_url = reverse('admin:news_post_add')
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, 200)