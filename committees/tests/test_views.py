from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from committees.models import Committee

class CommitteesIndexViewTest(TestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username="testuser1", email="user1@example.com", password="password")
        self.user2 = User.objects.create_user(username="testuser2", email="user2@example.com", password="password")
        
        # Create groups and committees
        self.group1 = Group.objects.create(name="Committee 1")
        self.committee1 = Committee.objects.create(
            group=self.group1,
            slug="committee-1",
            description="Committee 1 description",
            contact_person=self.user1,
            email="committee1@example.com"
        )
        
        self.group2 = Group.objects.create(name="Committee 2")
        self.committee2 = Committee.objects.create(
            group=self.group2,
            slug="committee-2",
            description="Committee 2 description",
            contact_person=self.user2,
            email="committee2@example.com"
        )
        
        # URL for the index view
        self.url = reverse('committees:index')
        
    def test_index_view_status_code(self):
        """Test that the index view returns a 200 status code."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_index_view_template(self):
        """Test that the index view uses the correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'committees/index.html')
    
    def test_index_view_context(self):
        """Test that the index view provides the correct context."""
        response = self.client.get(self.url)
        self.assertIn('committee_list', response.context)
        self.assertEqual(len(response.context['committee_list']), 2)
        
    def test_committees_ordered_correctly(self):
        """Test that committees are ordered correctly."""
        response = self.client.get(self.url)
        committees = response.context['committee_list']
        # Check that both committees are in the list
        self.assertTrue(self.committee1 in committees)
        self.assertTrue(self.committee2 in committees)


class CommitteesDetailViewTest(TestCase):
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
        
        # Add user to the committee's group
        self.group.user_set.add(self.user)
        
        # URL for the detail view
        self.url = reverse('committees:detail', kwargs={'slug': self.committee.slug})
        
    def test_detail_view_status_code(self):
        """Test that the detail view returns a 200 status code for an existing committee."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_detail_view_404(self):
        """Test that the detail view returns a 404 status code for a non-existent committee."""
        url = reverse('committees:detail', kwargs={'slug': 'non-existent-committee'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_detail_view_template(self):
        """Test that the detail view uses the correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'committees/detail.html')
    
    def test_detail_view_context(self):
        """Test that the detail view provides the correct context."""
        response = self.client.get(self.url)
        self.assertIn('committee', response.context)
        self.assertEqual(response.context['committee'], self.committee)
        
    def test_detail_view_shows_members(self):
        """Test that the detail view shows the committee members."""
        response = self.client.get(self.url)
        self.assertContains(response, self.user.email)
