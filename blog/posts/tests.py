from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, SavedPost

class SavedPostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            post_type='DISCOVERY'
        )

    def test_saved_post_creation(self):
        saved_post = SavedPost.objects.create(user=self.user, post=self.post)
        self.assertEqual(SavedPost.objects.count(), 1)
        self.assertEqual(saved_post.user, self.user)
        self.assertEqual(saved_post.post, self.post)

    def test_saved_post_cascade_delete_post(self):
        SavedPost.objects.create(user=self.user, post=self.post)
        self.post.delete()
        self.assertEqual(SavedPost.objects.count(), 0)

    def test_saved_post_cascade_delete_user(self):
        SavedPost.objects.create(user=self.user, post=self.post)
        self.user.delete()
        self.assertEqual(SavedPost.objects.count(), 0)

    def test_saved_post_unique_together(self):
        SavedPost.objects.create(user=self.user, post=self.post)
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            SavedPost.objects.create(user=self.user, post=self.post)

class SavePostViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            post_type='DISCOVERY'
        )

    def test_save_post_authenticated(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('save_post', kwargs={'pk': self.post.pk}))
        self.assertEqual(SavedPost.objects.count(), 1)
        self.assertRedirects(response, reverse('dashboard'))

    def test_remove_post_authenticated(self):
        self.client.login(username='testuser', password='password123')
        SavedPost.objects.create(user=self.user, post=self.post)
        response = self.client.get(reverse('save_post', kwargs={'pk': self.post.pk}))
        self.assertEqual(SavedPost.objects.count(), 0)
        self.assertRedirects(response, reverse('dashboard'))

    def test_save_post_unauthenticated(self):
        response = self.client.get(reverse('save_post', kwargs={'pk': self.post.pk}))
        self.assertEqual(SavedPost.objects.count(), 0)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

class DashboardViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.post = Post.objects.create(
            title='Saved Post',
            content='Test content',
            post_type='DISCOVERY'
        )
        SavedPost.objects.create(user=self.user, post=self.post)

    def test_dashboard_authenticated(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Saved Post')
        self.assertTemplateUsed(response, 'posts/dashboard.html')

    def test_dashboard_unauthenticated(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

class SearchResultsViewTest(TestCase):
    def setUp(self):
        self.post1 = Post.objects.create(
            title='First Post',
            content='This is about Django.',
            post_type='DISCOVERY'
        )
        self.post2 = Post.objects.create(
            title='Second Post',
            content='This is about React.',
            post_type='DISCOVERY'
        )

    def test_search_results_with_query_matching_title(self):
        response = self.client.get(reverse('search_results'), {'q': 'First'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.post1, response.context['posts'])
        self.assertNotIn(self.post2, response.context['posts'])

    def test_search_results_with_query_matching_content(self):
        response = self.client.get(reverse('search_results'), {'q': 'Django'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.post1, response.context['posts'])
        self.assertNotIn(self.post2, response.context['posts'])

    def test_search_results_with_no_query(self):
        response = self.client.get(reverse('search_results'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['posts']), 0)
        self.assertIsNone(response.context['query'])

    def test_search_results_case_insensitive(self):
        response = self.client.get(reverse('search_results'), {'q': 'django'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.post1, response.context['posts'])
        self.assertNotIn(self.post2, response.context['posts'])
