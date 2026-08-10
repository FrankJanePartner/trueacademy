from django.contrib import admin
from django.utils.html import format_html
from .models import GalleryImage


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['thumbnail', 'title', 'year', 'category', 'is_active', 'created_at']
    list_filter = ['year', 'category', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['-year', '-created_at']
    readonly_fields = ['created_at', 'updated_at']

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: auto; object-fit: cover;" />', obj.image.url)
        return '-' 
    thumbnail.short_description = 'Preview'
