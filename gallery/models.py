from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from PIL import Image as PILImage


def validate_gallery_image(image):
    """Keep the validator referenced by migration 0004 importable.

    The current GalleryImage field deliberately does not configure this helper.
    """
    if not image:
        return

    image_file = getattr(image, 'file', image)
    try:
        position = image_file.tell()
        uploaded_image = PILImage.open(image_file)
        uploaded_image.verify()
    except Exception as exc:
        raise ValidationError('The uploaded file is not a valid image or is corrupted.') from exc
    finally:
        try:
            image_file.seek(position)
        except (UnboundLocalError, AttributeError, OSError):
            pass


def gallery_image_upload_to(instance, filename):
    category = instance.category.slug
    return f'gallery/{category}/{filename}'


class GalleryCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
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


class GalleryImage(models.Model):
    image = models.ImageField(
        upload_to=gallery_image_upload_to
    )

    category = models.ForeignKey(
        GalleryCategory,
        on_delete=models.PROTECT,
        related_name='images'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id}'
