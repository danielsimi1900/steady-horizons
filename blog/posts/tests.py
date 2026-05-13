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
        response = self.client.post(reverse('save_post', kwargs={'pk': self.post.pk}))
        self.assertEqual(SavedPost.objects.count(), 1)
        self.assertRedirects(response, reverse('dashboard'))

    def test_remove_post_authenticated(self):
        self.client.login(username='testuser', password='password123')
        SavedPost.objects.create(user=self.user, post=self.post)
        response = self.client.post(reverse('save_post', kwargs={'pk': self.post.pk}))
        self.assertEqual(SavedPost.objects.count(), 0)
        self.assertRedirects(response, reverse('dashboard'))

    def test_save_post_unauthenticated(self):
        response = self.client.post(reverse('save_post', kwargs={'pk': self.post.pk}))
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

class PostCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.url = reverse('post_create')

    def test_unauthenticated_access(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_authenticated_get(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_form.html')

    def test_valid_post_submission(self):
        self.client.login(username='testuser', password='password123')
        data = {
            'title': 'Test Recipe',
            'content': 'Test recipe content',
            'post_type': 'RECIPE',
            'carbs_per_serving': '10.5',
            'fiber': '3.0',
            'glycemic_index': 'Low'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.title, 'Test Recipe')
        self.assertEqual(float(post.net_carbs), 7.5)  # 10.5 - 3.0
        self.assertRedirects(response, reverse('post_list'))

        # Test success message
        from django.contrib.messages import get_messages
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Your thought has been posted!")

    def test_invalid_post_submission(self):
        self.client.login(username='testuser', password='password123')
        data = {
            'title': '',  # Missing title
            'content': 'Test content',
            'post_type': 'DISCOVERY'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(Post.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'title', 'This field is required.')
