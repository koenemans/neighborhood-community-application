from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
import datetime
from django.contrib.auth.models import User, Group, Permission
from committees.models import Committee
from activities.models import Activity


class ActivityPermissionsTest(TestCase):
    def setUp(self):
        # Create staff user
        self.user = User.objects.create_user(
            username="staff_user", email="staff@example.com", password="password"
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

        # Add user to committee group and give permission to add activities
        add_activity_permission = Permission.objects.get(codename="add_activity")
        self.group.user_set.add(self.user)
        self.group.permissions.add(add_activity_permission)
        self.group.save()

        self.activity = Activity.objects.create(
            title="Test Activity",
            slug="test-activity",
            content="Test content",
            start=timezone.now(),
            end=timezone.now() + datetime.timedelta(hours=2),
            location="Test Location",
            committee=self.committee,
        )

    def test_anonymous_cannot_create_activity(self):
        """Test that anonymous users cannot create activities."""
        create_url = reverse("admin:activities_activity_add")
        response = self.client.get(create_url)
        self.assertNotEqual(response.status_code, 200)

    def test_anonymous_can_view_activity(self):
        """Test that anonymous users can view activities."""
        detail_url = reverse("activities:detail", kwargs={"slug": self.activity.slug})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)

    def test_staff_can_create_activity(self):
        """Test that staff users can create activities."""
        self.client.login(username="staff_user", password="password")
        create_url = reverse("admin:activities_activity_add")
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, 200)

    def test_staff_user_cannot_edit_other_committee_activity(self):
        """Staff users should not edit activities from other committees."""
        # Create second user and committee
        second_user = User.objects.create_user(
            username="another_user", email="another@example.com", password="password"
        )
        second_user.is_staff = True
        second_user.save()

        second_group = Group.objects.create(name="Second Committee")
        Committee.objects.create(
            group=second_group,
            slug="second-committee",
            description="Another committee",
            contact_person=second_user,
            email="second@example.com",
        )

        change_permission = Permission.objects.get(codename="change_activity")
        second_group.user_set.add(second_user)
        second_group.permissions.add(change_permission)
        second_group.save()

        self.client.login(username="another_user", password="password")
        edit_url = reverse("admin:activities_activity_change", args=[self.activity.id])
        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 403)
