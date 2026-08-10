# Migration 0002: Add GalleryCategory table + nullable FK column on GalleryImage

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        # 1. Create GalleryCategory table
        migrations.CreateModel(
            name='GalleryCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True, blank=True)),
                ('description', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Gallery Category',
                'verbose_name_plural': 'Gallery Categories',
                'ordering': ['name'],
            },
        ),

        # 2. Add nullable FK column (old CharField stays for now, handled in 0003)
        migrations.AddField(
            model_name='galleryimage',
            name='category_fk',
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='images',
                to='gallery.gallerycategory',
            ),
        ),
    ]
