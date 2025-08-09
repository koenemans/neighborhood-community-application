import datetime
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group, Permission
from committees.models import Committee
from activities.models import Activity


class ActivityAdminTest(TestCase):
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

        # Add user to committee group and give correct permissions
        view_activity_permission = Permission.objects.get(codename="view_activity")
        change_activity_permission = Permission.objects.get(codename="change_activity")
        add_activity_permission = Permission.objects.get(codename="add_activity")
        self.group.user_set.add(self.user)
        self.group.permissions.add(
            view_activity_permission,
            change_activity_permission,
            add_activity_permission,
        )
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

        self.client.login(username="staff_user", password="password")

    def test_activity_listed_in_admin(self):
        """Test that activities are listed in the admin site."""
        response = self.client.get(reverse("admin:activities_activity_changelist"))
        self.assertContains(response, "Test Activity")

    def test_activity_admin_fields(self):
        """Test that the admin displays the correct fields for an activity."""
        response = self.client.get(
            reverse("admin:activities_activity_change", args=[self.activity.id])
        )
        self.assertContains(response, "Test Activity")
        self.assertContains(response, "Test content")
        self.assertContains(response, "Test Location")

    def test_activity_admin_validation(self):
        """Test that the admin form validates activity data."""
        # Try to create an activity with end before start
        invalid_data = {
            "title": "Invalid Activity",
            "content": "This activity has invalid dates",
            "committee": self.committee.id,
            "location": "Test Location",
            "start_0": "2023-05-05",  # Date
            "start_1": "10:00:00",  # Time
            "end_0": "2023-05-04",  # Earlier date
            "end_1": "10:00:00",  # Time
        }
        response = self.client.post(
            reverse("admin:activities_activity_add"), data=invalid_data
        )
        self.assertEqual(response.status_code, 200)  # Form displayed with errors
        self.assertContains(response, "error")  # Error message displayed
