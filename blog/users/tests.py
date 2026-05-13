from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages

class SignupViewTests(TestCase):
    def test_signup_view_get(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/signup.html')

        # Verify the info message is added
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.INFO)
        self.assertEqual(str(messages_list[0]), "Join Steady Horizons to curate your own personal recipe wall.")

    def test_signup_view_post_valid_form(self):
        # Initial user count
        self.assertEqual(User.objects.count(), 0)

        data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

        response = self.client.post(reverse('signup'), data)

        # Verify redirect
        self.assertRedirects(response, reverse('post_list'))

        # Verify user was created
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(username='testuser')

        # Verify user was logged in (session should have '_auth_user_id')
        self.assertEqual(str(self.client.session['_auth_user_id']), str(user.pk))

    def test_signup_view_post_invalid_form(self):
        # Initial user count
        self.assertEqual(User.objects.count(), 0)

        data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'differentpassword',
        }

        response = self.client.post(reverse('signup'), data)

        # Verify it doesn't redirect and shows form again
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/signup.html')

        # Verify form has errors
        self.assertTrue(response.context['form'].errors)

        # Verify no user was created
        self.assertEqual(User.objects.count(), 0)

        # Verify user is not logged in
        self.assertNotIn('_auth_user_id', self.client.session)
