from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from committees.models import Committee
from news.models import Post
import datetime
from django.utils import timezone

class NewsIndexViewTest(TestCase):
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
        
        # Create test posts
        self.post1 = Post.objects.create(
            title="Test Post 1",
            slug="test-post-1",
            content="Content for test post 1",
            committee=self.committee,
            created_at=timezone.now() - datetime.timedelta(days=1)
        )
        
        self.post2 = Post.objects.create(
            title="Test Post 2",
            slug="test-post-2",
            content="Content for test post 2",
            committee=self.committee
        )
        
        # URL for the index view
        self.url = reverse('news:index')
        
    def test_index_view_status_code(self):
        """Test that the index view returns a 200 status code."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_index_view_template(self):
        """Test that the index view uses the correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'news/index.html')
    
    def test_index_view_context(self):
        """Test that the index view provides the correct context."""
        response = self.client.get(self.url)
        self.assertIn('latest_posts_list', response.context)
        self.assertEqual(len(response.context['latest_posts_list']), 2)
    
    def test_posts_ordered_by_created_at(self):
        """Test that posts are ordered by created_at in descending order."""
        response = self.client.get(self.url)
        posts = response.context['latest_posts_list']
        self.assertEqual(posts[0], self.post2)  # Most recent post first
        self.assertEqual(posts[1], self.post1)  # Older post second


class NewsDetailViewTest(TestCase):
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
        
        # Create a test post
        self.post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            content="Content for test post",
            committee=self.committee
        )
        
        # URL for the detail view
        self.url = reverse('news:detail', kwargs={'slug': self.post.slug})
        
    def test_detail_view_status_code(self):
        """Test that the detail view returns a 200 status code for an existing post."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_detail_view_404(self):
        """Test that the detail view returns a 404 status code for a non-existent post."""
        url = reverse('news:detail', kwargs={'slug': 'non-existent-post'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_detail_view_template(self):
        """Test that the detail view uses the correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'news/detail.html')
    
    def test_detail_view_context(self):
        """Test that the detail view provides the correct context."""
        response = self.client.get(self.url)
        self.assertIn('post', response.context)
        self.assertEqual(response.context['post'], self.post)


class NewsArchiveViewTest(TestCase):
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
        
        # Create posts for different committees in different years/months
        # Committee 1 posts
        self.post1 = Post.objects.create(
            title="Post 1 for Committee 1 - 2023 January",
            slug="post-1-committee-1",
            content="Content for post 1",
            committee=self.committee1,
            created_at=datetime.datetime(2023, 1, 15, tzinfo=timezone.get_current_timezone())
        )
        
        self.post2 = Post.objects.create(
            title="Post 2 for Committee 1 - 2023 February",
            slug="post-2-committee-1",
            content="Content for post 2",
            committee=self.committee1,
            created_at=datetime.datetime(2023, 2, 15, tzinfo=timezone.get_current_timezone())
        )
        
        # Committee 2 posts
        self.post3 = Post.objects.create(
            title="Post 3 for Committee 2 - 2022 December",
            slug="post-3-committee-2",
            content="Content for post 3",
            committee=self.committee2,
            created_at=datetime.datetime(2022, 12, 15, tzinfo=timezone.get_current_timezone())
        )
        
        self.post4 = Post.objects.create(
            title="Post 4 for Committee 2 - 2023 January",
            slug="post-4-committee-2",
            content="Content for post 4",
            committee=self.committee2,
            created_at=datetime.datetime(2023, 1, 20, tzinfo=timezone.get_current_timezone())
        )
        
        # URL for the archive view
        self.url = reverse('news:archive')
        
    def test_archive_view_status_code(self):
        """Test that the archive view returns a 200 status code."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_archive_view_template(self):
        """Test that the archive view uses the correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'news/archive.html')
    
    def test_archive_view_context(self):
        """Test that the archive view provides the correct context."""
        response = self.client.get(self.url)
        self.assertIn('grouped_news', response.context)
        self.assertIn('all_committees', response.context)
        
        # Check years in grouped_news
        grouped_news = response.context['grouped_news']
        self.assertIn(2022, grouped_news)
        self.assertIn(2023, grouped_news)
        
        # Check committees in all_committees
        all_committees = response.context['all_committees']
        self.assertEqual(len(all_committees), 2)
        self.assertIn(self.committee1, all_committees)
        self.assertIn(self.committee2, all_committees)
    
    def test_archive_view_with_committee_filter(self):
        """Test that the archive view correctly filters posts by committee."""
        # Filter by committee1
        url = f"{self.url}?committee={self.committee1.slug}"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('filtered_committee', response.context)
        self.assertEqual(response.context['filtered_committee'], self.committee1)
        
        grouped_news = response.context['grouped_news']
        
        # Committee 1 had posts in 2023 (January and February)
        self.assertIn(2023, grouped_news)
        
        # Check January 2023 - should only have Committee 1's post
        january_posts = grouped_news[2023]['January']
        self.assertEqual(len(january_posts), 1)
        self.assertEqual(january_posts[0], self.post1)
        
        # Check February 2023 - should only have Committee 1's post
        february_posts = grouped_news[2023]['February']
        self.assertEqual(len(february_posts), 1)
        self.assertEqual(february_posts[0], self.post2)
        
        # 2022 should not be present for Committee 1
        self.assertNotIn(2022, grouped_news)