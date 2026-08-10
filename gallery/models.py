import os
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import get_valid_filename, slugify
from PIL import Image as PILImage


MAX_GALLERY_IMAGE_SIZE = 5 * 1024 * 1024
ALLOWED_GALLERY_IMAGE_FORMATS = {'JPEG', 'PNG', 'WEBP'}


def validate_gallery_image(image):
    """Validate gallery uploads for both Django Admin and the API."""
    if not image:
        return

    if image.size > MAX_GALLERY_IMAGE_SIZE:
        raise ValidationError('Image size must be 5 MB or smaller.')

    image_file = getattr(image, 'file', image)
    try:
        position = image_file.tell()
    except (AttributeError, OSError):
        position = None

    try:
        uploaded_image = PILImage.open(image_file)
        image_format = uploaded_image.format
        uploaded_image.verify()
    except Exception as exc:
        raise ValidationError('The uploaded file is not a valid image or is corrupted.') from exc
    finally:
        if position is not None:
            image_file.seek(position)

    if image_format not in ALLOWED_GALLERY_IMAGE_FORMATS:
        raise ValidationError('Unsupported image format. Use JPG, PNG, or WEBP.')


class GalleryCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Gallery Category'
        verbose_name_plural = 'Gallery Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


def gallery_image_upload_to(instance, filename):
    """Upload to media/gallery/<year>/<uuid>_<filename> to avoid collisions."""
    safe_filename = get_valid_filename(os.path.basename(filename))
    safe_name = f'{uuid.uuid4().hex}_{safe_filename}'
    year = getattr(instance, 'year', None) or 2025
    return f'gallery/{year}/{safe_name}'


class GalleryImage(models.Model):
    image = models.ImageField(
        upload_to=gallery_image_upload_to,
        validators=[validate_gallery_image],
    )
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    year = models.IntegerField()
    category = models.ForeignKey(
        GalleryCategory,
        on_delete=models.PROTECT,
        related_name='images',
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-year', '-created_at']

    def __str__(self):
        cat = self.category.name if self.category else 'Uncategorised'
        return f'{self.title or self.image.name} ({self.year}) — {cat}'
