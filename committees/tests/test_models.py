from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group
from committees.models import Committee

class CommitteeModelFieldTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="user@example.com", password="password")
        self.group = Group.objects.create(name="Test Committee")

    def test_email_field_validation(self):
        """Test that the email field is validated."""
        # Valid email
        committee = Committee(
            group=self.group,
            slug="test-committee",
            description="A test committee",
            contact_person=self.user,
            email="valid@example.com"
        )
        committee.full_clean()  # This should not raise any exceptions
        
        # Invalid email
        committee = Committee(
            group=self.group,
            slug="test-committee",
            description="A test committee",
            contact_person=self.user,
            email="invalid-email"
        )
        with self.assertRaises(ValidationError):
            committee.full_clean()

class CommitteeModelRelationshipTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="user@example.com", password="password")
        self.group = Group.objects.create(name="Test Committee")

        self.committee = Committee.objects.create(
            group=self.group,
            slug="test-committee",
            description="This is a test committee",
            contact_person=self.user,
            email="test@example.com"
        )

    def test_group_belongs_to_committee(self):
        self.assertEqual(self.committee.group, self.group)

    def test_user_belongs_to_committee(self):
        self.assertEqual(self.committee.contact_person, self.user)
        
    def test_committee_string_representation(self):
        """Test the string representation of a committee."""
        self.assertEqual(str(self.committee), "Test Committee")

class CommitteeModelGetAbsoluteUrlTest(TestCase):
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

    def test_get_absolute_url(self):
        """Test that the get_absolute_url method returns the correct URL."""
        expected_url = f"/committees/{self.committee.slug}/"
        self.assertEqual(self.committee.get_absolute_url(), expected_url)

class CommitteeModelSlugTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="user@example.com", password="password")
        self.group = Group.objects.create(name="Test Committee")

    def test_slug_generation(self):
        """Test that a slug is automatically generated if not provided."""
        committee = Committee.objects.create(
            group=self.group,
            description="A test committee",
            contact_person=self.user,
            email="test@example.com"
        )
        self.assertEqual(committee.slug, "test-committee")
        
    def test_unique_slug(self):
        """Test that slugs are unique."""
        # Create first committee
        Committee.objects.create(
            group=Group.objects.create(name="Sports Committee"),
            slug="sports-committee",
            description="A sports committee",
            contact_person=self.user,
            email="sports@example.com"
        )
        
        # Create second committee with same name (should get different slug)
        committee2 = Committee(
            group=Group.objects.create(name="Sports Committee 2"),
            description="Another sports committee",
            contact_person=self.user,
            email="sports2@example.com"
        )
        
        # This should raise a validation error because the slug would be the same
        with self.assertRaises(ValidationError):
            committee2.full_clean()
            committee2.save()