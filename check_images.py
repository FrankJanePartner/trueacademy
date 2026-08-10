import os
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trueacademy.settings')
django.setup()

from django.conf import settings
from gallery.models import GalleryImage

print('GalleryImage records and file status:')
for img in GalleryImage.objects.select_related('category').all():
    if img.image:
        full_path = Path(settings.MEDIA_ROOT) / img.image.name
        status = 'OK' if full_path.exists() else 'MISSING'
    else:
        full_path = None
        status = 'NO_IMAGE'
    cat = img.category.name if img.category else 'None'
    print(f'  [{status}] id={img.id} cat={cat} name={img.image.name!r}')
print('Done.')
