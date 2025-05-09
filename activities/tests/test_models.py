from django.test import TestCase
from activities.models import Activity
from committees.models import Committee
from django.contrib.auth.models import User, Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.utils import timezone
from django.core.exceptions import ValidationError
import tempfile
import datetime

class ActivityModelFieldTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="testuser", email="user@example.com", password="password")
        group = Group.objects.create(name="Test Committee")

        self.committee = Committee.objects.create(
            group=group,
            slug="test-committee",
            description="A test committee",
            contact_person=user,
            email="test@example.com"
        )

    def test_title_max_length(self):
        """Test that the title field has a max_length of 200."""
        activity = Activity(
            title="A" * 201,  # Exceeding max_length of 200
            slug="test-activity",
            content="Test content",
            start=timezone.now(),
            end=timezone.now() + datetime.timedelta(hours=2),
            location="Test Location",
            committee=self.committee
        )
        with self.assertRaises(ValidationError):
            activity.full_clean()

    def test_string_representation(self):
        """Test the string representation of the activity."""
        activity = Activity.objects.create(
            title="Test String Activity",
            slug="test-string-activity",
            content="Test content",
            start=timezone.now() + datetime.timedelta(hours=1),
            end=timezone.now() + datetime.timedelta(hours=3),
            location="Test Location",
            committee=self.committee
        )
        self.assertEqual(str(activity), "Test String Activity")

class ActivityModelRelationshipTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="testuser", email="user@example.com", password="password")
        group = Group.objects.create(name="Test Committee")

        self.committee = Committee.objects.create(
            group=group,
            slug="test-committee",
            description="A test committee",
            contact_person=user,
            email="test@example.com"
        )

        self.activity = Activity.objects.create(
            title="Test Activity",
            slug="test-activity",
            content="Test content",
            start=timezone.now(),
            end=timezone.now() + datetime.timedelta(hours=2),
            location="Test Location",
            committee=self.committee
        )

    def test_activity_belongs_to_committee(self):
        """Test that the activity belongs to the correct committee."""
        self.assertEqual(self.activity.committee, self.committee)

class ActivityModelGetAbsoluteUrlTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="testuser", email="user@example.com", password="password")
        group = Group.objects.create(name="Test Committee")

        self.committee = Committee.objects.create(
            group=group,
            slug="test-committee",
            description="A test committee",
            contact_person=user,
            email="test@example.com"
        )

        self.activity = Activity.objects.create(
            title="Test Activity",
            slug="test-activity",
            content="Test content",
            start=timezone.now(),
            end=timezone.now() + datetime.timedelta(hours=2),
            location="Test Location",
            committee=self.committee
        )

    def test_get_absolute_url(self):
        """Test that the get_absolute_url method returns the correct URL."""
        expected_url = f"/activities/{self.activity.slug}/"
        self.assertEqual(self.activity.get_absolute_url(), expected_url)

class ActivityModelSlugTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="testuser", email="user@example.com", password="password")
        group = Group.objects.create(name="Test Committee")

        self.committee = Committee.objects.create(
            group=group,
            slug="test-committee",
            description="A test committee",
            contact_person=user,
            email="test@example.com"
        )

    def test_slug_generation(self):
        """Test that the slug is generated correctly."""
        activity = Activity.objects.create(
            title="Test Activity",
            content="Test content",
            start=timezone.now(),
            end=timezone.now() + datetime.timedelta(hours=2),
            location="Test Location",
            committee=self.committee
        )
        self.assertEqual(activity.slug, "test-activity")

class ActivityModelOrderingTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="testuser", email="user@example.com", password="password")
        group = Group.objects.create(name="Test Committee")

        self.committee = Committee.objects.create(
            group=group,
            slug="test-committee",
            description="A test committee",
            contact_person=user,
            email="test@example.com"
        )

        self.activity1 = Activity.objects.create(
            title="Second Activity",
            slug="second-activity",
            content="This is the second activity",
            start=timezone.now() + datetime.timedelta(days=7),
            end=timezone.now() + datetime.timedelta(days=7) + datetime.timedelta(hours=2),
            location="Test Location",
            committee=self.committee
        )

        self.activity2 = Activity.objects.create(
            title="First Activity",
            slug="first-activity",
            content="This is the first activity",
            start=timezone.now() + datetime.timedelta(days=2),
            end=timezone.now() + datetime.timedelta(days=2) + datetime.timedelta(hours=2),
            location="Test Location",
            committee=self.committee
        )

    def test_default_ordering(self):
        """Test that activities are ordered by start date."""
        activities = Activity.objects.all()
        self.assertEqual(activities[0], self.activity2)  # First to start should be first
        self.assertEqual(activities[1], self.activity1)  # Second to start should be last

@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class ActivityModelPosterTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="testuser", email="user@example.com", password="password")
        group = Group.objects.create(name="Test Committee")

        self.committee = Committee.objects.create(
            group=group,
            slug="test-committee",
            description="A test committee",
            contact_person=user,
            email="test@example.com"
        )

    def test_poster_upload(self):
        """Test that the poster can be uploaded and saved correctly."""
        poster = SimpleUploadedFile("poster.jpg", b"file_content", content_type="image/jpeg")
        activity = Activity.objects.create(
            title="Test Activity",
            slug="test-activity",
            content="Test content",
            start=timezone.now(),
            end=timezone.now() + datetime.timedelta(hours=2),
            location="Test Location",
            committee=self.committee,
            poster=poster
        )
        self.assertTrue(activity.poster.name.startswith("poster"))

class ActivityModelStartDate(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="testuser", email="user@example.com", password="password")
        group = Group.objects.create(name="Test Committee")

        self.committee = Committee.objects.create(
            group=group,
            slug="test-committee",
            description="A test committee",
            contact_person=user,
            email="test@example.com"
        )

    def test_start_in_past(self):
        """Test that the start date cannot be in the past."""
        start = timezone.now() - datetime.timedelta(days=1)
        activity = Activity(
                title="Test Activity",
                slug="test-activity",
                content="Test content",
                start=start,
                end=start + datetime.timedelta(hours=2),
                location="Test Location",
                committee=self.committee
            )
        with self.assertRaises(ValidationError):
            activity.full_clean()
       

    def test_start_in_future(self):
        """Test that the start date can be in the future."""
        start = timezone.now() + datetime.timedelta(days=1)
        activity = Activity(
            title="Test Activity",
            slug="test-activity",
            content="Test content",
            start=start,
            end=start + datetime.timedelta(hours=2),
            location="Test Location",
            committee=self.committee
        )
        self.assertEqual(activity.start, start)

class ActivityModelEndDate(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="testuser", email="user@example.com", password="password")
        group = Group.objects.create(name="Test Committee")

        self.committee = Committee.objects.create(
            group=group,
            slug="test-committee",
            description="A test committee",
            contact_person=user,
            email="test@example.com"
        )

    def test_end_after_start(self):
        """Test that the end date is after the start date."""
        start = timezone.now()
        end = start + datetime.timedelta(hours=2)
        activity = Activity(
            title="Test Activity",
            slug="test-activity",
            content="Test content",
            start=start,
            end=end,
            location="Test Location",
            committee=self.committee
        )
        self.assertEqual(activity.end, end)

    def test_end_same_as_start(self):
        """Test that the end date can be the same as the start date."""
        start = timezone.now()
        end = start
        activity = Activity(
            title="Test Activity",
            slug="test-activity",
            content="Test content",
            start=start,
            end=end,
            location="Test Location",
            committee=self.committee
        )
        self.assertEqual(activity.end, start)

    def test_end_before_start(self):
        """Test that the end date cannot be before the start date."""
        start = timezone.now()
        end = start - datetime.timedelta(hours=2)
        activity = Activity(
            title="Test Activity",
            slug="test-activity",
            content="Test content",
            start=start,
            end=end,
            location="Test Location",
            committee=self.committee
        )
        with self.assertRaises(ValidationError):
            activity.full_clean()
