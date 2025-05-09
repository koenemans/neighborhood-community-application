from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group, Permission
from committees.models import Committee

class CommitteeAdminTest(TestCase):
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
        view_committee_permission = Permission.objects.get(codename='view_committee')
        change_committee_permission = Permission.objects.get(codename='change_committee')
        self.user.user_permissions.add(view_committee_permission, change_committee_permission)
        self.user.save()
        
        # Login user
        self.client.login(username='staff_user', password='password')
        
    def test_committee_listed_in_admin(self):
        """Test that committees are listed in the admin site."""
        response = self.client.get(reverse('admin:committees_committee_changelist'))
        self.assertContains(response, "Test Committee")
        
    def test_committee_admin_fields(self):
        """Test that the admin displays the correct fields for a committee."""
        response = self.client.get(reverse('admin:committees_committee_change', args=[self.committee.id]))
        self.assertContains(response, "Test Committee")
        self.assertContains(response, "A test committee")
        self.assertContains(response, "test@example.com")
