from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from committees.models import Committee
from activities.models import Activity
from django.utils import timezone
import datetime

class ActivitiesTemplateTest(TestCase):
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
        
        # Create test activity
        self.activity = Activity.objects.create(
            title="Test Activity Title",
            slug="test-activity",
            content="Test content with some formatting",
            start=timezone.now() + datetime.timedelta(days=1),
            end=timezone.now() + datetime.timedelta(days=2),
            location="Test Location",
            committee=self.committee
        )
        
    def test_index_template_displays_activities(self):
        """Test that the index template displays activities correctly."""
        response = self.client.get(reverse('activities:index'))
        self.assertContains(response, "Test Activity Title")
        self.assertContains(response, "Test Location")
        
    def test_detail_template_displays_activity_content(self):
        """Test that the detail template displays activity content correctly."""
        response = self.client.get(reverse('activities:detail', kwargs={'slug': self.activity.slug}))
        self.assertContains(response, "Test Activity Title")
        self.assertContains(response, "Test content with some formatting")
        self.assertContains(response, "Test Location")
        
    def test_archive_template_contains_filter_options(self):
        """Test that the archive template displays filter options."""
        response = self.client.get(reverse('activities:archive'))
        self.assertContains(response, "Filter by Committee")
        self.assertContains(response, "Test Committee")  # Committee name