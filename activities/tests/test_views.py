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
        """Test that activities are ordered by start date (soonest first)."""
        response = self.client.get(self.url)
        activities = response.context['upcoming_activity_list']
        self.assertEqual(len(activities), 2)
        self.assertEqual(activities[0], self.activity1)  # First upcoming activity first
        self.assertEqual(activities[1], self.activity2)  # Second upcoming activity second
        # Explicitly verify ordering is by start date
        self.assertTrue(activities[0].start < activities[1].start)


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
        # Verify activity data is correctly provided
        self.assertEqual(response.context['activity'].title, "Test Activity")
        self.assertEqual(response.context['activity'].location, "Test Location")


class ActivitiesArchiveViewTest(TestCase):
    def setUp(self):
        # Create users and committees
        self.user1 = User.objects.create_user(username="testuser1", email="user1@example.com", password="password")
        self.group1 = Group.objects.create(name="Committee 1")
        self.committee1 = Committee.objects.create(
            group=self.group1,
            slug="committee-1",
            description="Committee 1 description",
            contact_person=self.user1,
            email="committee1@example.com"
        )
        
        self.user2 = User.objects.create_user(username="testuser2", email="user2@example.com", password="password")
        self.group2 = Group.objects.create(name="Committee 2")
        self.committee2 = Committee.objects.create(
            group=self.group2,
            slug="committee-2",
            description="Committee 2 description",
            contact_person=self.user2,
            email="committee2@example.com"
        )
        
        # Create activities for different committees in different years/months
        # Committee 1 activities
        self.activity1 = Activity.objects.create(
            title="Activity 1 for Committee 1 - 2023 January",
            slug="activity-1-committee-1",
            content="Content for activity 1",
            start=datetime.datetime(2023, 1, 15, tzinfo=timezone.get_current_timezone()),
            end=datetime.datetime(2023, 1, 15, 2, 0, tzinfo=timezone.get_current_timezone()),
            location="Location 1",
            committee=self.committee1,
            created_at=datetime.datetime(2023, 1, 15, tzinfo=timezone.get_current_timezone())
        )
        
        self.activity2 = Activity.objects.create(
            title="Activity 2 for Committee 1 - 2023 February",
            slug="activity-2-committee-1",
            content="Content for activity 2",
            start=datetime.datetime(2023, 2, 15, tzinfo=timezone.get_current_timezone()),
            end=datetime.datetime(2023, 2, 15, 2, 0, tzinfo=timezone.get_current_timezone()),
            location="Location 2",
            committee=self.committee1,
            created_at=datetime.datetime(2023, 2, 15, tzinfo=timezone.get_current_timezone())
        )
        
        # Committee 2 activities
        self.activity3 = Activity.objects.create(
            title="Activity 3 for Committee 2 - 2022 December",
            slug="activity-3-committee-2",
            content="Content for activity 3",
            start=datetime.datetime(2022, 12, 15, tzinfo=timezone.get_current_timezone()),
            end=datetime.datetime(2022, 12, 15, 2, 0, tzinfo=timezone.get_current_timezone()),
            location="Location 3",
            committee=self.committee2,
            created_at=datetime.datetime(2022, 12, 15, tzinfo=timezone.get_current_timezone())
        )
        
        self.activity4 = Activity.objects.create(
            title="Activity 4 for Committee 2 - 2023 January",
            slug="activity-4-committee-2",
            content="Content for activity 4",
            start=datetime.datetime(2023, 1, 20, tzinfo=timezone.get_current_timezone()),
            end=datetime.datetime(2023, 1, 20, 2, 0, tzinfo=timezone.get_current_timezone()),
            location="Location 4",
            committee=self.committee2,
            created_at=datetime.datetime(2023, 1, 20, tzinfo=timezone.get_current_timezone())
        )
        
        # URL for the archive view
        self.url = reverse('activities:archive')
        
    def test_archive_view_status_code(self):
        """Test that the archive view returns a 200 status code."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_archive_view_template(self):
        """Test that the archive view uses the correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'activities/archive.html')
    
    def test_archive_view_context(self):
        """Test that the archive view provides the correct context."""
        response = self.client.get(self.url)
        self.assertIn('grouped_activities', response.context)
        self.assertIn('all_committees', response.context)
        
        # Check years in grouped_activities
        grouped_activities = response.context['grouped_activities']
        self.assertIn(2022, grouped_activities)
        self.assertIn(2023, grouped_activities)
        
        # Check committees in all_committees
        all_committees = response.context['all_committees']
        self.assertEqual(len(all_committees), 2)
        self.assertIn(self.committee1, all_committees)
        self.assertIn(self.committee2, all_committees)
    
    def test_archive_view_with_committee_filter(self):
        """Test that the archive view correctly filters activities by committee."""
        # Filter by committee1
        url = f"{self.url}?committee={self.committee1.slug}"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('filtered_committee', response.context)
        self.assertEqual(response.context['filtered_committee'], self.committee1)
        
        grouped_activities = response.context['grouped_activities']
        
        # Committee 1 had activities in 2023 (January and February)
        self.assertIn(2023, grouped_activities)
        
        # Check January 2023 - should only have Committee 1's activity
        january_activities = grouped_activities[2023]['January']
        self.assertEqual(len(january_activities), 1)
        self.assertEqual(january_activities[0], self.activity1)
        
        # Check February 2023 - should only have Committee 1's activity
        february_activities = grouped_activities[2023]['February']
        self.assertEqual(len(february_activities), 1)
        self.assertEqual(february_activities[0], self.activity2)
        
        # 2022 should not be present for Committee 1
        self.assertNotIn(2022, grouped_activities)