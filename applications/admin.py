from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'location', 'cohort', 'status', 'submitted_at']
    search_fields = ['full_name', 'email', 'phone', 'location', 'cohort']
    list_filter = ['status', 'cohort', 'experience', 'involvement', 'submitted_at']
    ordering = ['-submitted_at']
    readonly_fields = ['submitted_at', 'updated_at']
