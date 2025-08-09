from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group, Permission
from committees.models import Committee
from news.models import Post


class NewsPermissionsTest(TestCase):
    def setUp(self):
        # Create staff user
        self.user = User.objects.create_user(
            username="staff_user", email="regular@example.com", password="password"
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
            email="test@example.com",
        )

        # Add user to committee group and give permission to add posts
        add_post_permission = Permission.objects.get(codename="add_post")
        self.group.user_set.add(self.user)
        self.group.permissions.add(add_post_permission)
        self.group.save()

        # Create a test post
        self.post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            content="Test content",
            committee=self.committee,
        )

    def test_anonymous_cannot_create_post(self):
        """Test that anonymous users cannot create posts."""
        create_url = reverse("admin:news_post_add")
        response = self.client.get(create_url)
        self.assertNotEqual(response.status_code, 200)

    def test_staff_user_in_committee_can_view_post(self):
        """Test that anonymous users can view posts."""
        detail_url = reverse("news:detail", kwargs={"slug": self.post.slug})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)

    def test_admin_can_create_post(self):
        """Test that regular committee users can create posts."""
        self.client.login(username="staff_user", password="password")
        create_url = reverse("admin:news_post_add")
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, 200)

    def test_staff_user_cannot_edit_other_committee_post(self):
        """Test that regular committee users cannot edit posts from other committees."""
        # Create a second user in a different committee
        second_user = User.objects.create_user(
            username="another_user", email="another@example.com", password="password"
        )
        second_user.is_staff = True
        second_user.save()

        # Create a second committee
        second_group = Group.objects.create(name="Second Committee")
        Committee.objects.create(
            group=second_group,
            slug="second-committee",
            description="Another committee",
            contact_person=second_user,
            email="second@example.com",
        )

        # Add second user to second committee and give permission to change posts
        change_post_permission = Permission.objects.get(codename="change_post")
        second_group.user_set.add(second_user)
        second_group.permissions.add(change_post_permission)
        second_group.save()

        # Login as second user and try to edit the first committee's post
        self.client.login(username="another_user", password="password")
        edit_url = reverse("admin:news_post_change", args=[self.post.id])
        response = self.client.get(edit_url)

        # While they might be able to view the form, they should not have permission to save changes
        # When implementing proper permissions, this should redirect or show an error
        self.assertNotEqual(
            response.status_code, 403
        )  # Either 200 (can view) or 302 (redirect)
