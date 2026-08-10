# Migration 0003: Data migration — create category records, map existing images,
# then drop old CharField and rename FK column to 'category'.

import django.db.models.deletion
from django.db import migrations, models


# ─── Forward data migration ──────────────────────────────────────────────────

LEGACY_CATEGORIES = [
    {'name': 'Workshop',    'slug': 'workshop',    'description': 'Practical workshops and training sessions.'},
    {'name': 'Graduation',  'slug': 'graduation',  'description': 'Cohort graduation ceremonies and celebrations.'},
    {'name': 'Event',       'slug': 'event',       'description': 'Campus events, conferences, and leadership sessions.'},
    {'name': 'Other',       'slug': 'other',       'description': 'Other campus moments.'},
]

SLUG_MAP = {
    'workshop':   'workshop',
    'graduation': 'graduation',
    'event':      'event',
    'other':      'other',
}


def create_categories_and_map_images(apps, schema_editor):
    GalleryCategory = apps.get_model('gallery', 'GalleryCategory')
    GalleryImage = apps.get_model('gallery', 'GalleryImage')

    # Create the 4 default categories
    cat_by_slug = {}
    for cat_data in LEGACY_CATEGORIES:
        cat, _ = GalleryCategory.objects.get_or_create(
            slug=cat_data['slug'],
            defaults={
                'name': cat_data['name'],
                'description': cat_data['description'],
                'is_active': True,
            },
        )
        cat_by_slug[cat.slug] = cat

    # Map every existing GalleryImage to its category FK
    for img in GalleryImage.objects.all():
        old_slug = (img.category or 'other').lower()
        mapped_slug = SLUG_MAP.get(old_slug, 'other')
        img.category_fk = cat_by_slug[mapped_slug]
        img.save()


def reverse_migration(apps, schema_editor):
    """Reverse: restore the category string from the FK slug."""
    GalleryImage = apps.get_model('gallery', 'GalleryImage')
    for img in GalleryImage.objects.select_related('category_fk').all():
        if img.category_fk:
            img.category = img.category_fk.slug
            img.save()


# ─── Migration definition ─────────────────────────────────────────────────────

class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_gallerycategory'),
    ]

    operations = [
        # 1. Run data migration
        migrations.RunPython(
            create_categories_and_map_images,
            reverse_migration,
        ),

        # 2. Remove the old CharField
        migrations.RemoveField(
            model_name='galleryimage',
            name='category',
        ),

        # 3. Rename category_fk -> category
        migrations.RenameField(
            model_name='galleryimage',
            old_name='category_fk',
            new_name='category',
        ),

        # 4. Make the FK non-nullable (all images now have a category)
        migrations.AlterField(
            model_name='galleryimage',
            name='category',
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='images',
                to='gallery.gallerycategory',
            ),
        ),
    ]
