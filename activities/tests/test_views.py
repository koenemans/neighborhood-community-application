from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from committees.models import Committee
from activities.models import Activity
import datetime
from django.utils import timezone

class ActivitiesIndexViewTest(TestCase):
    def setUp(self):
        # Create user and committee
        self.user = User.objects.create_user(username="testuser", email="user@example.com", password="password")
        self.group = Group.objects.create(name="Test Committee")
        self.committee = Committee.objects.create(
            group=self.group,
            slug="test-committee",
            description="A test committee",
            contact_person=self.user,
            email="test@example.com"
        )
        
        # Create test activities
        self.activity1 = Activity.objects.create(
            title="Test Activity 1",
            slug="test-activity-1",
            content="Content for test activity 1",
            start=timezone.now() + datetime.timedelta(days=1),
            end=timezone.now() + datetime.timedelta(days=1) + datetime.timedelta(hours=2),
            location="Test Location 1",
            committee=self.committee,
        )
        
        self.activity2 = Activity.objects.create(
            title="Test Activity 2",
            slug="test-activity-2",
            content="Content for test activity 2",
            start=timezone.now() + datetime.timedelta(days=2),
            end=timezone.now() + datetime.timedelta(days=2) + datetime.timedelta(hours=2),
            location="Test Location 2",
            committee=self.committee
        )
        
        # URL for the index view
        self.url = reverse('activities:index')
        
    def test_index_view_status_code(self):
        """Test that the index view returns a 200 status code."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_index_view_template(self):
        """Test that the index view uses the correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'activities/index.html')
    
    def test_index_view_context(self):
        """Test that the index view provides the correct context."""
        response = self.client.get(self.url)
        self.assertIn('upcoming_activity_list', response.context)
        self.assertEqual(len(response.context['upcoming_activity_list']), 2)
    
    def test_activities_ordered_by_start_date(self):
        """Test that activities are ordered correctly."""
        response = self.client.get(self.url)
        activities = response.context['upcoming_activity_list']
        self.assertEqual(activities[0].title, "Test Activity 1")  # First upcoming activity first
        self.assertEqual(activities[1].title, "Test Activity 2")  # Second upcoming activity second


class ActivitiesDetailViewTest(TestCase):
    def setUp(self):
        # Create user and committee
        self.user = User.objects.create_user(username="testuser", email="user@example.com", password="password")
        self.group = Group.objects.create(name="Test Committee")
        self.committee = Committee.objects.create(
            group=self.group,
            slug="test-committee",
            description="A test committee",
            contact_person=self.user,
            email="test@example.com"
        )
        
        # Create a test activity
        self.activity = Activity.objects.create(
            title="Test Activity",
            slug="test-activity",
            content="Content for test activity",
            start=timezone.now(),
            end=timezone.now() + datetime.timedelta(hours=2),
            location="Test Location",
            committee=self.committee
        )
        
        # URL for the detail view
        self.url = reverse('activities:detail', kwargs={'slug': self.activity.slug})
        
    def test_detail_view_status_code(self):
        """Test that the detail view returns a 200 status code for an existing activity."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_detail_view_404(self):
        """Test that the detail view returns a 404 status code for a non-existent activity."""
        url = reverse('activities:detail', kwargs={'slug': 'non-existent-activity'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_detail_view_template(self):
        """Test that the detail view uses the correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'activities/detail.html')
    
    def test_detail_view_context(self):
        """Test that the detail view provides the correct context."""
        response = self.client.get(self.url)
        self.assertIn('activity', response.context)
        self.assertEqual(response.context['activity'], self.activity)