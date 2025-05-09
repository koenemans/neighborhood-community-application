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
        self.user = User.objects.create_user(username="staff_user", email="staff@example.com", password="password")
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
        
        # Add user to committee group and give permission to add activities
        add_activity_permission = Permission.objects.get(codename='add_activity')
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
            committee=self.committee
        )
        
    def test_anonymous_cannot_create_activity(self):
        """Test that anonymous users cannot create activities."""
        create_url = reverse('admin:activities_activity_add')
        response = self.client.get(create_url)
        self.assertNotEqual(response.status_code, 200)
        
    def test_anonymous_can_view_activity(self):
        """Test that anonymous users can view activities."""
        detail_url = reverse('activities:detail', kwargs={'slug': self.activity.slug})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        
    def test_staff_can_create_activity(self):
        """Test that staff users can create activities."""
        self.client.login(username="staff_user", password="password")
        create_url = reverse('admin:activities_activity_add')
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, 200)