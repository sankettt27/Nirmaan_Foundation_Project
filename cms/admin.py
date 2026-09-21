"""
cms/admin.py — Django Admin registration for CMS models.

Provides a fallback admin interface for managing CMS content
via Django's built-in admin panel at /admin/.
"""

from django.contrib import admin
from .models import Banner, VisionMission, Statistic, Initiative


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'created_at')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'subtitle')
    ordering = ('order',)


@admin.register(VisionMission)
class VisionMissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'section_type', 'order', 'is_active', 'created_at')
    list_filter = ('section_type', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'content')
    ordering = ('section_type', 'order')


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ('label', 'value', 'order', 'is_active', 'created_at')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
    search_fields = ('label', 'value')
    ordering = ('order',)


@admin.register(Initiative)
class InitiativeAdmin(admin.ModelAdmin):
    list_display = ('title', 'tag', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'tag')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description')
    ordering = ('order',)
