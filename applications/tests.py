import json

from django.contrib.auth import get_user_model
from django.test import Client, TestCase


class ApplicationCsrfTests(TestCase):
    def test_logged_in_browser_can_submit_application_with_csrf_token(self):
        user = get_user_model().objects.create_user(username='csrf-user', password='safe-password')
        client = Client(enforce_csrf_checks=True)
        client.force_login(user)

        bootstrap_response = client.get('/api/csrf/')
        self.assertEqual(bootstrap_response.status_code, 200)
        csrf_token = client.cookies['csrftoken'].value

        response = client.post(
            '/api/applications/',
            data=json.dumps({
                'full_name': 'CSRF Applicant',
                'phone': '+234 800 000 0000',
                'email': 'applicant@example.com',
                'location': 'Lagos',
                'involvement': 'Student',
                'attend_all': 'yes',
                'ethics_commitment': 'yes',
                'heard_from': 'Website',
                'refer_friends': 'no',
                'referral_numbers': '',
                'cohort': 'CSRF Test Cohort',
            }),
            content_type='application/json',
            HTTP_X_CSRFTOKEN=csrf_token,
        )
        self.assertEqual(response.status_code, 201)
