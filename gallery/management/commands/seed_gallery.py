"""
management command: seed_gallery

Imports all static gallery assets from static/core/asset/ into Django MEDIA storage.

Behaviour:
- Creates GalleryCategory records for the 4 default slugs (idempotent).
- For each asset entry:
    - Get-or-create the GalleryImage record by title.
    - If the record exists but the media file is missing: copy the asset and repair it.
    - If the record exists and the file is OK: skip.
    - If the record does not exist: create it and copy the file.
- Safe to run multiple times — never creates duplicates.

Usage:
    python manage.py seed_gallery
"""

import os
import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from gallery.models import GalleryCategory, GalleryImage


ASSETS = [
    # Workshops
    {'filename': 'workshops-1.jpg', 'title': 'Real Estate Strategy Session',    'category_slug': 'workshop',   'year': 2025},
    {'filename': 'workshops-2.jpg', 'title': 'Field Practical & Inspection',    'category_slug': 'workshop',   'year': 2025},
    {'filename': 'workshops-3.jpg', 'title': 'Property Development Masterclass','category_slug': 'workshop',   'year': 2025},
    {'filename': 'workshops-4.jpg', 'title': 'Marketing & Sales Workshop',      'category_slug': 'workshop',   'year': 2024},
    {'filename': 'workshops-5.jpg', 'title': 'Negotiation Skills Training',     'category_slug': 'workshop',   'year': 2024},
    {'filename': 'workshops-6.jpg', 'title': 'Legal Frameworks in Real Estate', 'category_slug': 'workshop',   'year': 2024},
    {'filename': 'workshops-7.jpg', 'title': 'Investment Analysis Workshop',    'category_slug': 'workshop',   'year': 2024},
    {'filename': 'workshops-8.jpg', 'title': 'Property Management Practical',   'category_slug': 'workshop',   'year': 2024},

    # Graduation
    {'filename': 'graduation-1.jpg', 'title': 'Cohort Graduation Ceremony',    'category_slug': 'graduation', 'year': 2025},
    {'filename': 'graduation-2.jpg', 'title': 'Certificate Presentation',      'category_slug': 'graduation', 'year': 2025},
    {'filename': 'graduation-3.jpg', 'title': 'Graduate Group Photo',          'category_slug': 'graduation', 'year': 2025},
    {'filename': 'graduation-4.jpg', 'title': 'Excellence Award Winner',       'category_slug': 'graduation', 'year': 2023},
    {'filename': 'graduation-5.jpg', 'title': 'Cohort 3 Graduation',           'category_slug': 'graduation', 'year': 2023},
    {'filename': 'graduation-6.jpg', 'title': 'Mentorship Recognition',        'category_slug': 'graduation', 'year': 2023},
    {'filename': 'graduation-7.jpg', 'title': 'Alumni Network Celebration',    'category_slug': 'graduation', 'year': 2023},
    {'filename': 'graduation-8.jpg', 'title': 'Keynote & Celebration',         'category_slug': 'graduation', 'year': 2023},

    # Leadership / Events
    {'filename': 'leadership 1.png', 'title': 'Leadership Summit Session',     'category_slug': 'event',      'year': 2025},
    {'filename': 'leadership 2.png', 'title': 'Executive Panel Discussion',    'category_slug': 'event',      'year': 2025},
    {'filename': 'leadership 3.png', 'title': 'Guest Speaker Keynote',         'category_slug': 'event',      'year': 2025},
    {'filename': 'leadership 4.png', 'title': 'Industry Networking Forum',     'category_slug': 'event',      'year': 2024},
    {'filename': 'leadership 5.png', 'title': 'Mentorship Round Table',        'category_slug': 'event',      'year': 2024},
]


def _media_file_exists(image_field) -> bool:
    """Return True if the media file actually exists on disk."""
    if not image_field or not image_field.name:
        return False
    full_path = Path(settings.MEDIA_ROOT) / image_field.name
    return full_path.exists()


def _copy_to_media(src_path: Path, dest_relative: str) -> str:
    """
    Copy src_path to MEDIA_ROOT / dest_relative.
    Creates parent directories if needed.
    Returns the relative path used (dest_relative).
    """
    dest_abs = Path(settings.MEDIA_ROOT) / dest_relative
    dest_abs.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(src_path), str(dest_abs))
    return dest_relative


class Command(BaseCommand):
    help = 'Import static gallery assets into Django MEDIA storage and repair broken records.'

    def handle(self, *args, **options):
        asset_dir = Path(settings.BASE_DIR) / 'static' / 'core' / 'asset'
        media_root = Path(settings.MEDIA_ROOT)

        # ── 1. Ensure default GalleryCategory records exist ─────────────────
        default_categories = [
            {'name': 'Workshop',   'slug': 'workshop',   'description': 'Practical workshops and training sessions.'},
            {'name': 'Graduation', 'slug': 'graduation', 'description': 'Cohort graduation ceremonies.'},
            {'name': 'Event',      'slug': 'event',      'description': 'Campus events and leadership sessions.'},
            {'name': 'Other',      'slug': 'other',      'description': 'Other campus moments.'},
        ]
        categories = {}
        for cat_data in default_categories:
            cat, created = GalleryCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description'],
                    'is_active': True,
                },
            )
            categories[cat.slug] = cat
            if created:
                self.stdout.write(f'  Created category: {cat.name}')

        # ── 2. Process each asset entry ──────────────────────────────────────
        imported = 0
        repaired = 0
        skipped = 0

        for entry in ASSETS:
            src_path = asset_dir / entry['filename']
            if not src_path.exists():
                self.stdout.write(
                    self.style.WARNING(f'  [MISSING SRC] {entry["filename"]} not found in static assets — skipped.')
                )
                skipped += 1
                continue

            category = categories.get(entry['category_slug'])
            title = entry['title']
            year = entry['year']

            # Determine target media relative path
            _, ext = os.path.splitext(entry['filename'])
            safe_filename = entry['filename'].replace(' ', '_')
            dest_relative = f'gallery/{year}/{safe_filename}'

            existing = GalleryImage.objects.filter(title=title).first()

            if existing:
                file_ok = _media_file_exists(existing.image)
                if file_ok:
                    # Nothing to do
                    skipped += 1
                    continue
                else:
                    # Repair: copy file, update image field
                    _copy_to_media(src_path, dest_relative)
                    existing.image = dest_relative
                    existing.category = category
                    existing.year = year
                    existing.is_active = True
                    existing.save()
                    self.stdout.write(f'  [REPAIRED]  {title}')
                    repaired += 1
            else:
                # Create new record
                _copy_to_media(src_path, dest_relative)
                GalleryImage.objects.create(
                    image=dest_relative,
                    title=title,
                    description=f'Photos from Trinity Real Estate University — {entry["category_slug"]} {year}.',
                    category=category,
                    year=year,
                    is_active=True,
                )
                self.stdout.write(f'  [IMPORTED]  {title}')
                imported += 1

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'Done.  Imported: {imported}  |  Repaired: {repaired}  |  Skipped: {skipped}'
        ))
