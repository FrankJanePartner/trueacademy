from io import BytesIO
from tempfile import TemporaryDirectory

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import Client, TestCase, override_settings
from PIL import Image
from rest_framework.test import APIClient

from .models import GalleryCategory, GalleryImage


def make_image(name='gallery.png'):
    buffer = BytesIO()
    Image.new('RGB', (20, 20), color='navy').save(buffer, format='PNG')
    return SimpleUploadedFile(name, buffer.getvalue(), content_type='image/png')


class GalleryApiTests(TestCase):
    def setUp(self):
        self.media_directory = TemporaryDirectory()
        self.media_settings = override_settings(MEDIA_ROOT=self.media_directory.name)
        self.media_settings.enable()
        self.addCleanup(self.media_settings.disable)
        self.addCleanup(self.media_directory.cleanup)

        self.client = APIClient()
        self.workshops = GalleryCategory.objects.get(slug='workshop')
        self.events = GalleryCategory.objects.get(slug='event')
        self.image = GalleryImage.objects.create(
            image=make_image(),
            category=self.workshops,
        )

    def test_public_gallery_returns_uploaded_images_and_categories(self):
        categories = self.client.get('/api/gallery/categories/')
        self.assertEqual(categories.status_code, 200)
        self.assertTrue({'workshop', 'event'}.issubset(
            {item['slug'] for item in categories.json()}
        ))

        response = self.client.get('/api/gallery/')
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual([item['id'] for item in payload], [self.image.id])
        self.assertEqual(payload[0]['category']['slug'], 'workshop')
        self.assertTrue(payload[0]['image_url'].startswith('/media/gallery/workshop/'))

    def test_admin_upload_is_available_to_the_frontend_through_media_url(self):
        user = get_user_model().objects.create_user(
            username='gallery-admin', password='safe-password', is_staff=True
        )
        self.client.force_authenticate(user=user)
        response = self.client.post(
            '/api/gallery/',
            {'category_id': self.events.id, 'image': make_image('event.png')},
            format='multipart',
        )
        self.assertEqual(response.status_code, 201)
        image_url = response.json()['image_url']
        self.assertTrue(image_url.startswith('/media/gallery/event/'))

        media_response = self.client.get(image_url)
        self.assertEqual(media_response.status_code, 200)
        self.assertTrue(media_response['Content-Type'].startswith('image/'))

    def test_django_admin_can_upload_an_image(self):
        user = get_user_model().objects.create_superuser(
            username='admin', email='admin@example.com', password='safe-password'
        )
        client = Client()
        client.force_login(user)
        response = client.post(
            '/admin/gallery/galleryimage/add/',
            {'category': self.events.id, 'image': make_image('admin-event.png')},
        )
        self.assertEqual(response.status_code, 302)
        uploaded = GalleryImage.objects.get(image__endswith='/admin-event.png')
        self.assertEqual(uploaded.category, self.events)


class SeedGalleryCommandTests(TestCase):
    def test_seed_is_idempotent_and_repairs_a_missing_file(self):
        with TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                call_command('seed_gallery')
                image_count = GalleryImage.objects.count()
                self.assertGreater(image_count, 0)

                seeded = GalleryImage.objects.first()
                seeded.image.storage.delete(seeded.image.name)
                call_command('seed_gallery')

                seeded.refresh_from_db()
                self.assertEqual(GalleryImage.objects.count(), image_count)
                self.assertTrue(seeded.image.storage.exists(seeded.image.name))
