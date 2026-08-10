from django.db import models


def gallery_image_upload_to(instance, filename):
    return f'gallery/{instance.year}/{filename}'


class GalleryImage(models.Model):
    CATEGORY_WORKSHOP = 'workshop'
    CATEGORY_GRADUATION = 'graduation'
    CATEGORY_EVENT = 'event'
    CATEGORY_OTHER = 'other'

    CATEGORY_CHOICES = [
        (CATEGORY_WORKSHOP, 'Workshop'),
        (CATEGORY_GRADUATION, 'Graduation'),
        (CATEGORY_EVENT, 'Event'),
        (CATEGORY_OTHER, 'Other'),
    ]

    image = models.ImageField(upload_to=gallery_image_upload_to)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    year = models.IntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=CATEGORY_OTHER)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-year', '-created_at']

    def __str__(self):
        return f"{self.title or self.image.name} ({self.year})"
