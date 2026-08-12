"""Import bundled gallery images into the media storage.

The command is optional and safe to run repeatedly. It matches the simplified
gallery model: every image only belongs to a category and has its upload path.
"""

import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from gallery.models import GalleryCategory, GalleryImage


CATEGORY_SOURCES = {
    'workshop': ('Workshop', 'workshops-*'),
    'graduation': ('Graduation', 'graduation-*'),
    'event': ('Event', 'leadership *'),
}


class Command(BaseCommand):
    help = 'Import bundled gallery assets into media storage.'

    def handle(self, *args, **options):
        asset_directory = Path(settings.BASE_DIR) / 'static' / 'core' / 'asset'
        media_root = Path(settings.MEDIA_ROOT)
        imported = repaired = skipped = 0

        for slug, (name, filename_pattern) in CATEGORY_SOURCES.items():
            category, _ = GalleryCategory.objects.get_or_create(
                slug=slug,
                defaults={'name': name},
            )

            for source in asset_directory.glob(filename_pattern):
                if source.suffix.lower() not in {'.jpg', '.jpeg', '.png', '.webp'}:
                    continue

                safe_filename = source.name.replace(' ', '_')
                relative_path = f'gallery/{slug}/{safe_filename}'
                destination = media_root / relative_path
                image = GalleryImage.objects.filter(
                    image__endswith=f'/{safe_filename}'
                ).first()

                if image and destination.exists():
                    if image.category_id != category.id:
                        image.category = category
                        image.save(update_fields=['category'])
                    skipped += 1
                    continue

                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)

                if image:
                    image.image = relative_path
                    image.category = category
                    image.save(update_fields=['image', 'category'])
                    repaired += 1
                else:
                    GalleryImage.objects.create(image=relative_path, category=category)
                    imported += 1

        self.stdout.write(self.style.SUCCESS(
            f'Done. Imported: {imported} | Repaired: {repaired} | Skipped: {skipped}'
        ))
