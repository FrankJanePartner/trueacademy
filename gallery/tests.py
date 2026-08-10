from io import BytesIO
from tempfile import TemporaryDirectory

from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from PIL import Image
from rest_framework.test import APIClient

from .models import GalleryCategory, GalleryImage
from .admin import GalleryImageAdmin


def make_image(name='gallery.png', image_format='PNG'):
    buffer = BytesIO()
    Image.new('RGB', (20, 20), color='navy').save(buffer, format=image_format)
    return SimpleUploadedFile(name, buffer.getvalue(), content_type=f'image/{image_format.lower()}')


class GalleryApiTests(TestCase):
    def setUp(self):
        self.media_directory = TemporaryDirectory()
        self.media_settings = override_settings(MEDIA_ROOT=self.media_directory.name)
        self.media_settings.enable()
        self.addCleanup(self.media_settings.disable)
        self.addCleanup(self.media_directory.cleanup)

        self.client = APIClient()
        self.workshops = GalleryCategory.objects.get(slug='workshop')
        self.inactive_category = GalleryCategory.objects.create(
            name='Archived Events', slug='archived-events', is_active=False
        )
        self.public_image = GalleryImage.objects.create(
            title='Public image',
            image=make_image(),
            category=self.workshops,
            year=2026,
        )
        self.hidden_by_category = GalleryImage.objects.create(
            title='Hidden category image',
            image=make_image('hidden-category.png'),
            category=self.inactive_category,
            year=2026,
        )
        self.inactive_image = GalleryImage.objects.create(
            title='Inactive image',
            image=make_image('inactive.png'),
            category=self.workshops,
            year=2026,
            is_active=False,
        )

    def test_public_endpoints_only_expose_active_images_and_categories(self):
        category_response = self.client.get('/api/gallery/categories/')
        self.assertEqual(category_response.status_code, 200)
        self.assertNotIn('archived-events', [item['slug'] for item in category_response.json()])

        response = self.client.get('/api/gallery/')
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual([item['id'] for item in payload], [self.public_image.id])
        self.assertEqual(payload[0]['category']['slug'], 'workshop')
        self.assertTrue(payload[0]['image_url'].startswith('/media/gallery/2026/'))

        self.assertEqual(self.client.get(f'/api/gallery/{self.inactive_image.id}/').status_code, 404)
        self.assertEqual(self.client.get(f'/api/gallery/{self.hidden_by_category.id}/').status_code, 404)

    def test_image_writes_require_an_administrator_and_validate_uploads(self):
        post_data = {
            'title': 'Annual Conference',
            'year': 2026,
            'category_id': self.workshops.id,
            'image': make_image('conference.png'),
        }
        self.assertEqual(self.client.post('/api/gallery/', post_data, format='multipart').status_code, 403)

        user = get_user_model().objects.create_user(
            username='gallery-admin', password='safe-password', is_staff=True
        )
        self.client.force_authenticate(user=user)
        response = self.client.post(
            '/api/gallery/',
            {
                'title': 'Annual Conference',
                'year': 2026,
                'category_id': self.workshops.id,
                'image': make_image('conference.png'),
            },
            format='multipart',
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['category']['slug'], 'workshop')

        invalid = SimpleUploadedFile('not-an-image.jpg', b'not an image', content_type='image/jpeg')
        invalid_response = self.client.post(
            '/api/gallery/',
            {
                'title': 'Invalid upload',
                'year': 2026,
                'category_id': self.workshops.id,
                'image': invalid,
            },
            format='multipart',
        )
        self.assertEqual(invalid_response.status_code, 400)
        self.assertIn('image', invalid_response.json())

    def test_django_admin_form_accepts_supported_uploads_and_rejects_gif(self):
        admin_form_class = GalleryImageAdmin(GalleryImage, AdminSite()).get_form(None)
        form_data = {
            'title': 'Admin upload',
            'year': 2026,
            'category': self.workshops.id,
            'is_active': 'on',
        }
        valid_form = admin_form_class(data=form_data, files={'image': make_image('admin-upload.webp', 'WEBP')})
        self.assertTrue(valid_form.is_valid(), valid_form.errors)

        gif_form = admin_form_class(data=form_data, files={'image': make_image('not-supported.gif', 'GIF')})
        self.assertFalse(gif_form.is_valid())
        self.assertIn('image', gif_form.errors)


class SeedGalleryCommandTests(TestCase):
    def test_seed_is_idempotent_and_repairs_a_missing_file(self):
        with TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                from django.core.management import call_command

                call_command('seed_gallery')
                self.assertEqual(GalleryImage.objects.count(), 21)
                seeded = GalleryImage.objects.get(title='Real Estate Strategy Session')
                self.assertTrue(seeded.image.storage.exists(seeded.image.name))

                seeded.image.storage.delete(seeded.image.name)
                self.assertFalse(seeded.image.storage.exists(seeded.image.name))
                call_command('seed_gallery')

                seeded.refresh_from_db()
                self.assertEqual(GalleryImage.objects.count(), 21)
                self.assertTrue(seeded.image.storage.exists(seeded.image.name))
