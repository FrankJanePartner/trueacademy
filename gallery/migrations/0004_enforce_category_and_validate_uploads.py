import django.db.models.deletion
import gallery.models
from django.db import migrations, models


def assign_uncategorised_images(apps, schema_editor):
    """Defensively preserve old rows before enforcing the required category."""
    GalleryCategory = apps.get_model('gallery', 'GalleryCategory')
    GalleryImage = apps.get_model('gallery', 'GalleryImage')

    other, _ = GalleryCategory.objects.get_or_create(
        slug='other',
        defaults={
            'name': 'Other',
            'description': 'Other campus moments.',
            'is_active': True,
        },
    )
    GalleryImage.objects.filter(category__isnull=True).update(category=other)


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_migrate_categories'),
    ]

    operations = [
        migrations.RunPython(assign_uncategorised_images, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='galleryimage',
            name='category',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='images',
                to='gallery.gallerycategory',
            ),
        ),
        migrations.AlterField(
            model_name='galleryimage',
            name='image',
            field=models.ImageField(
                upload_to=gallery.models.gallery_image_upload_to,
                validators=[gallery.models.validate_gallery_image],
            ),
        ),
    ]
