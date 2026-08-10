from django.contrib import admin
from django.utils.html import format_html

from .models import GalleryCategory, GalleryImage


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'image_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']

    def image_count(self, obj):
        return obj.images.filter(is_active=True).count()
    image_count.short_description = 'Active Images'


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['thumbnail', 'title', 'category', 'year', 'is_active', 'created_at']
    list_filter = ['category', 'year', 'is_active', 'created_at']
    list_editable = ['is_active']
    search_fields = ['title', 'description']
    ordering = ['-year', '-created_at']
    readonly_fields = ['image_preview', 'created_at', 'updated_at']
    autocomplete_fields = ['category']

    fieldsets = (
        ('Image', {
            'fields': ('image', 'image_preview'),
        }),
        ('Details', {
            'fields': ('title', 'description', 'category', 'year'),
        }),
        ('Status', {
            'fields': ('is_active',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def thumbnail(self, obj):
        if obj.image:
            try:
                return format_html(
                    '<img src="{}" style="width:80px;height:60px;object-fit:cover;border-radius:4px;" />',
                    obj.image.url
                )
            except Exception:
                return '(missing file)'
        return '—'
    thumbnail.short_description = 'Preview'

    def image_preview(self, obj):
        if obj.image:
            try:
                return format_html(
                    '<img src="{}" style="max-width:400px;max-height:300px;object-fit:contain;" />',
                    obj.image.url
                )
            except Exception:
                return '(file missing)'
        return '—'
    image_preview.short_description = 'Image Preview'
