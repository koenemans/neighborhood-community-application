from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from committees.models import Committee

class CommitteesTemplateTest(TestCase):
    def setUp(self):
        # Setup user and committee
        self.user = User.objects.create_user(
            username="testuser", 
            email="user@example.com", 
            password="password",
            first_name="Test",
            last_name="User"
        )
        self.group = Group.objects.create(name="Test Committee")
        self.committee = Committee.objects.create(
            group=self.group,
            slug="test-committee",
            description="This is a test committee with detailed description.",
            contact_person=self.user,
            email="test@example.com"
        )
        
        # Add user to the committee's group
        self.group.user_set.add(self.user)
        
    def test_index_template_displays_committees(self):
        """Test that the index template displays committees correctly."""
        response = self.client.get(reverse('committees:index'))
        self.assertContains(response, "Test Committee")
        self.assertContains(response, "This is a test committee")
        
    def test_detail_template_displays_committee_content(self):
        """Test that the detail template displays committee content correctly."""
        response = self.client.get(reverse('committees:detail', kwargs={'slug': self.committee.slug}))
        self.assertContains(response, "Test Committee")
        self.assertContains(response, "This is a test committee with detailed description")
        self.assertContains(response, "test@example.com")
        
    def test_detail_template_displays_committee_members(self):
        """Test that the detail template displays committee members."""
        response = self.client.get(reverse('committees:detail', kwargs={'slug': self.committee.slug}))
        self.assertContains(response, "Test User")
        self.assertContains(response, "user@example.com")
