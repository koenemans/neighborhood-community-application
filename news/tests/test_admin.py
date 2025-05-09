from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group, Permission
from committees.models import Committee
from news.models import Post

class NewsAdminTest(TestCase):
    def setUp(self):
        # Create staff user
        self.user = User.objects.create_user(
            username="staff_user",
            email="staff@example.com",
            password="password"
        )
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
        
        # Add user to committee group and give correct permissions
        view_post_permission = Permission.objects.get(codename='view_post')
        change_post_permission = Permission.objects.get(codename='change_post')
        add_post_permission = Permission.objects.get(codename='add_post')
        self.group.user_set.add(self.user)
        self.group.permissions.add(
            view_post_permission,
            change_post_permission,
            add_post_permission
        )
        self.group.save()
        
        # Create a test post
        self.post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            content="Test content",
            committee=self.committee
        )
        
        # Login user
        self.client.login(username='staff_user', password='password')
        
    def test_post_listed_in_admin(self):
        """Test that posts are listed in the admin site."""
        response = self.client.get(reverse('admin:news_post_changelist'))
        self.assertContains(response, "Test Post")
        
    def test_post_admin_fields(self):
        """Test that the admin displays the correct fields for a post."""
        response = self.client.get(reverse('admin:news_post_change', args=[self.post.id]))
        self.assertContains(response, "Test Post")
        self.assertContains(response, "Test content")
        
    def test_post_admin_validation(self):
        """Test that the admin form validates post data."""
        # Try to create a post with an invalid title (too long)
        invalid_data = {
            'title': 'A' * 201,  # Exceeding max_length of 200
            'content': 'Test content',
            'committee': self.committee.id,
        }
        response = self.client.post(reverse('admin:news_post_add'), data=invalid_data)
        self.assertEqual(response.status_code, 200)  # Form displayed with errors
        self.assertContains(response, "error")  # Error message displayed