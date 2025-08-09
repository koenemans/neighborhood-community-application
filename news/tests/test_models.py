from django.test import TestCase
from news.models import Post

from committees.models import Committee
from django.contrib.auth.models import User, Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
import tempfile
import re


class PostModelFieldTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="testuser", email="user@example.com", password="password"
        )
        group = Group.objects.create(name="Test Committee")

        self.committee = Committee.objects.create(
            group=group,
            slug="test-committee",
            description="A test committee",
            contact_person=user,
            email="test@example.com",
        )

    def test_title_max_length(self):
        """Test that the title field has a max_length of 200."""
        post = Post.objects.create(
            title="A" * 201,  # Exceeding max_length of 200
            slug="test-post",
            content="Test content",
            committee=self.committee,
        )
        with self.assertRaises(Exception):
            post.full_clean()  # This will raise a ValidationError


class PostModelRelationshipTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="testuser", email="user@example.com", password="password"
        )
        group = Group.objects.create(name="Test Committee")

        self.committee = Committee.objects.create(
            group=group,
            slug="test-committee",
            description="A test committee",
            contact_person=user,
            email="test@example.com",
        )

        self.post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            content="Test content",
            committee=self.committee,
        )

    def test_post_belongs_to_committee(self):
        """Test that the post belongs to the correct committee."""
        self.assertEqual(self.post.committee, self.committee)


class PostModelGetAbsoluteUrlTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="testuser", email="user@example.com", password="password"
        )
        group = Group.objects.create(name="Test Committee")

        self.committee = Committee.objects.create(
            group=group,
            slug="test-committee",
            description="A test committee",
            contact_person=user,
            email="test@example.com",
        )

        self.post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            content="Test content",
            committee=self.committee,
        )

    def test_get_absolute_url(self):
        """Test that the get_absolute_url method returns the correct URL."""
        expected_url = f"/news/{self.post.slug}/"
        self.assertEqual(self.post.get_absolute_url(), expected_url)


class PostModelSlugTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="testuser", email="user@example.com", password="password"
        )
        group = Group.objects.create(name="Test Committee")

        self.committee = Committee.objects.create(
            group=group,
            slug="test-committee",
            description="A test committee",
            contact_person=user,
            email="test@example.com",
        )

    def test_slug_generation(self):
        """Test that the slug is generated correctly from the title."""
        post = Post.objects.create(
            title="Test Post", content="Test content", committee=self.committee
        )
        self.assertEqual(post.slug, "test-post")


class PostModelOrderingTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="testuser", email="user@example.com", password="password"
        )
        group = Group.objects.create(name="Test Committee")

        self.committee = Committee.objects.create(
            group=group,
            slug="test-committee",
            description="A test committee",
            contact_person=user,
            email="test@example.com",
        )

        self.post1 = Post.objects.create(
            title="Older Post",
            slug="older-post",
            content="Older content",
            committee=self.committee,
        )

        self.post2 = Post.objects.create(
            title="Newer Post",
            slug="newer-post",
            content="Newer content",
            committee=self.committee,
        )

    def test_default_ordering(self):
        """Test that posts are ordered by created_at in descending order."""
        posts = Post.objects.all()
        self.assertEqual(posts[0], self.post2)
        self.assertEqual(posts[1], self.post1)


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class PostModelPosterTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="testuser", email="user@example.com", password="password"
        )
        group = Group.objects.create(name="Test Committee")

        self.committee = Committee.objects.create(
            group=group,
            slug="test-committee",
            description="A test committee",
            contact_person=user,
            email="test@example.com",
        )

    def test_poster_upload(self):
        """Test that the poster field can accept an image file."""
        poster = SimpleUploadedFile(
            "poster.jpg", b"file_content", content_type="image/jpeg"
        )
        post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            content="Test content",
            committee=self.committee,
            poster=poster,
        )
        year = post.created_at.strftime("%Y")
        month = post.created_at.strftime("%m")
        day = post.created_at.strftime("%d")
        file_hash = re.search(r"\_(.*?)\.", post.poster.name).group(1)
        self.assertEqual(
            post.poster.name,
            f"news/posters/{year}/{month}/{day}/poster_{file_hash}.jpg",
        )


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class PostModelAttachmentTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="testuser", email="user@example.com", password="password"
        )
        group = Group.objects.create(name="Test Committee")

        self.committee = Committee.objects.create(
            group=group,
            slug="test-committee",
            description="A test committee",
            contact_person=user,
            email="test@example.com",
        )

    def test_attachment_upload(self):
        """Test that the attachment can be uploaded and saved correctly."""
        attachment = SimpleUploadedFile(
            "document.pdf", b"file_content", content_type="application/pdf"
        )
        post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            content="Test content",
            committee=self.committee,
            attachment=attachment,
        )
        year = post.created_at.strftime("%Y")
        month = post.created_at.strftime("%m")
        day = post.created_at.strftime("%d")
        file_hash = re.search(r"\_(.*?)\.", post.attachment.name).group(1)
        self.assertEqual(
            post.attachment.name,
            f"news/attachments/{year}/{month}/{day}/document_{file_hash}.pdf",
        )


class PostModelStringRepresentation(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="testuser", email="user@example.com", password="password"
        )
        group = Group.objects.create(name="Test Committee")

        self.committee = Committee.objects.create(
            group=group,
            slug="test-committee",
            description="A test committee",
            contact_person=user,
            email="test@example.com",
        )

    def test_string_representation(self):
        """Test the string representation of a post."""
        post = Post.objects.create(
            title="Test Post Title",
            slug="test-post",
            content="Test content",
            committee=self.committee,
        )
        self.assertEqual(str(post), "Test Post Title")
