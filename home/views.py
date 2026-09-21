"""
home/views.py — Views for the public-facing Home (landing page) application.

Assignment 2 update: Now queries CMS models for dynamic content.
Falls back to static content if no CMS data exists.
"""
from django.shortcuts import render


def index(request):
    """
    Render the Nirmaan Foundation public landing page.

    Queries the CMS models for dynamic content:
    - Banners (hero section slider)
    - Vision & Mission statements
    - Impact statistics
    - Initiatives / Programs

    Falls back to static HTML content when no CMS data is available.
    """
    from cms.models import Banner, Initiative, Statistic, VisionMission

    banners = Banner.objects.filter(is_active=True).order_by('order')
    vision_items = VisionMission.objects.filter(section_type='vision', is_active=True).order_by('order')
    mission_items = VisionMission.objects.filter(section_type='mission', is_active=True).order_by('order')
    statistics = Statistic.objects.filter(is_active=True).order_by('order')
    initiatives = Initiative.objects.filter(is_active=True).order_by('order')

    context = {
        'banners': banners,
        'vision_items': vision_items,
        'mission_items': mission_items,
        'statistics': statistics,
        'initiatives': initiatives,
        # Flags for template to decide: use CMS data or static fallback
        'has_banners': banners.exists(),
        'has_statistics': statistics.exists(),
        'has_initiatives': initiatives.exists(),
    }
    return render(request, 'home/index.html', context)
