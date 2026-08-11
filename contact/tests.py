import json

from django.contrib.auth import get_user_model
from django.test import Client, TestCase


class ContactCsrfTests(TestCase):
    def test_logged_in_browser_can_submit_contact_form_with_csrf_token(self):
        user = get_user_model().objects.create_user(username='csrf-user', password='safe-password')
        client = Client(enforce_csrf_checks=True)
        client.force_login(user)

        self.assertEqual(client.post('/api/contact/', data='{}', content_type='application/json').status_code, 403)

        bootstrap_response = client.get('/api/csrf/')
        self.assertEqual(bootstrap_response.status_code, 200)
        csrf_token = client.cookies['csrftoken'].value

        response = client.post(
            '/api/contact/',
            data=json.dumps({
                'full_name': 'CSRF Contact',
                'email': 'contact@example.com',
                'phone': '+234 800 000 0000',
                'subject': 'CSRF test',
                'message': 'This submission includes Django’s CSRF token.',
            }),
            content_type='application/json',
            HTTP_X_CSRFTOKEN=csrf_token,
        )
        self.assertEqual(response.status_code, 201)
