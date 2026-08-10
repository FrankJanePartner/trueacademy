import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trueacademy.settings')
django.setup()

from applications.serializers import ApplicationSerializer

payload = {
    'full_name': 'Test User',
    'phone': '+2348000000000',
    'email': 'test@example.com',
    'location': 'Lagos, Lagos State',
    'involvement': 'interested',
    'experience': 'none',
    'interests': ['Land Sales'],
    'challenge': 'I want to learn.',
    'attend_all': 'yes',
    'ethics_commitment': 'yes',
    'heard_from': 'instagram',
    'refer_friends': 'no',
    'referral_numbers': '',
    'submitted_at': '2026-08-10T08:34:00Z',
    'cohort': 'Cohort 4'
}
serializer = ApplicationSerializer(data=payload)
print('is_valid:', serializer.is_valid())
print('errors:', json.dumps(serializer.errors, indent=2))
