from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group, Permission
from committees.models import Committee

class CommitteePermissionsTest(TestCase):
    def setUp(self):
        # Create staff user
        self.staff_user = User.objects.create_user(
            username="staff_user", 
            email="staff@example.com", 
            password="password"
        )
        self.staff_user.is_staff = True
        self.staff_user.save()

        # Create regular user
        self.regular_user = User.objects.create_user(
            username="regular_user", 
            email="regular@example.com", 
            password="password"
        )
        
        # Setup committee
        self.group = Group.objects.create(name="Test Committee")
        self.committee = Committee.objects.create(
            group=self.group,
            slug="test-committee",
            description="A test committee",
            contact_person=self.staff_user,
            email="test@example.com"
        )
        
        # Add permissions to view and change committees
        view_committee_permission = Permission.objects.get(codename='view_committee')
        change_committee_permission = Permission.objects.get(codename='change_committee')
        self.group.permissions.add(view_committee_permission, change_committee_permission)
        
        # Add staff user to the committee group
        self.group.user_set.add(self.staff_user)
        self.group.save()
        
    def test_anonymous_can_view_committee(self):
        """Test that anonymous users can view committees."""
        detail_url = reverse('committees:detail', kwargs={'slug': self.committee.slug})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        
    def test_anonymous_cannot_access_admin(self):
        """Test that anonymous users cannot access the admin site."""
        admin_url = reverse('admin:committees_committee_changelist')
        response = self.client.get(admin_url)
        self.assertNotEqual(response.status_code, 200)
        
    def test_staff_can_access_admin(self):
        """Test that staff users can access the admin site."""
        self.client.login(username="staff_user", password="password")
        admin_url = reverse('admin:committees_committee_changelist')
        response = self.client.get(admin_url)
        self.assertEqual(response.status_code, 200)
        
    def test_regular_user_cannot_access_admin(self):
        """Test that regular users cannot access the admin site."""
        self.client.login(username="regular_user", password="password")
        admin_url = reverse('admin:committees_committee_changelist')
        response = self.client.get(admin_url)
        self.assertNotEqual(response.status_code, 200)
