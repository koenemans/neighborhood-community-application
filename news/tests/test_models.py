from django.test import TestCase
from news.models import Post

from committees.models import Committee
from django.contrib.auth.models import User,Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
import tempfile

class PostModelFieldTest(TestCase):
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
        post = Post.objects.create(
            title="A" * 201,  # Exceeding max_length of 200
            slug="test-post",
            content="Test content",
            committee=self.committee
        )
        with self.assertRaises(Exception):
            post.full_clean()  # This will raise a ValidationError

class PostModelRelationshipTest(TestCase):
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

        self.post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            content="Test content",
            committee=self.committee
        )

    def test_post_belongs_to_committee(self):
        self.assertEqual(self.post.committee, self.committee)

class PostModelGetAbsoluteUrlTest(TestCase):
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

        self.post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            content="Test content",
            committee=self.committee
        )

    def test_get_absolute_url(self):
        expected_url = f"/news/{self.post.slug}/"
        self.assertEqual(self.post.get_absolute_url(), expected_url)

class PostModelSlugTest(TestCase):
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
        post = Post.objects.create(
            title="Test Post",
            content="Test content",
            committee=self.committee
        )
        self.assertEqual(post.slug, "test-post")

class PostModelOrderingTest(TestCase):
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

        self.post1 = Post.objects.create(
            title="Older Post",
            slug="older-post",
            content="Older content",
            committee=self.committee
        )

        self.post2 = Post.objects.create(
            title="Newer Post",
            slug="newer-post",
            content="Newer content",
            committee=self.committee
        )

    def test_default_ordering(self):
        posts = Post.objects.all()
        self.assertEqual(posts[0], self.post2)
        self.assertEqual(posts[1], self.post1)

@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class PostModelPosterTest(TestCase):
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
        poster = SimpleUploadedFile("poster.jpg", b"file_content", content_type="image/jpeg")
        post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            content="Test content",
            committee=self.committee,
            poster=poster
        )
        self.assertTrue(post.poster.name.startswith("poster"))