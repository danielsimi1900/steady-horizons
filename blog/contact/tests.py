from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from .forms import ContactForm

class ContactViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('contact')

    def test_contact_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')
        self.assertIsInstance(response.context['form'], ContactForm)

    def test_contact_view_post_valid_data(self):
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message.'
        }
        response = self.client.post(self.url, data)

        self.assertRedirects(response, self.url)

        self.assertEqual(len(mail.outbox), 1)

        self.assertEqual(mail.outbox[0].subject, 'Test Subject')
        self.assertIn('This is a test message.', mail.outbox[0].body)
        self.assertIn('test@example.com', mail.outbox[0].body)
        self.assertEqual(mail.outbox[0].from_email, 'test@example.com')
        self.assertEqual(mail.outbox[0].to, ['admin@t1dsteadyhorizons.com'])

        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Thank you for sharing! We've received your message.")

    def test_contact_view_post_invalid_data(self):
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            # missing message
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')

        self.assertTrue(response.context['form'].errors)

        self.assertEqual(len(mail.outbox), 0)
