from django.contrib import admin
from django.utils.html import format_html

from .models import GalleryCategory, GalleryImage


admin.site.register(GalleryCategory)
admin.site.register(GalleryImage)