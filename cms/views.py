"""
cms/views.py — Admin CMS Views for Home Page Content Management.

Assignment 2: Content Management System

All views are protected by `role_required('admin')` — only admin users
can access these pages. Provides full CRUD for:
  - Banners (hero section slider)
  - Vision & Mission content
  - Impact Statistics
  - Initiatives / Programs

URL namespace: cms
Base path: /dashboard/admin/home/
"""

from functools import wraps

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.views import role_required

from .forms import BannerForm, InitiativeForm, StatisticForm, VisionMissionForm
from .models import Banner, Initiative, Statistic, VisionMission


# ─────────────────────────────────────────────────────────────
# CMS DASHBOARD — OVERVIEW
# ─────────────────────────────────────────────────────────────

@role_required('admin')
def cms_dashboard_view(request):
    """
    CMS Overview page — shows counts of all content items
    with quick-add buttons for each section.
    """
    context = {
        'banner_count': Banner.objects.count(),
        'banner_active': Banner.objects.filter(is_active=True).count(),
        'vm_count': VisionMission.objects.count(),
        'vm_active': VisionMission.objects.filter(is_active=True).count(),
        'stat_count': Statistic.objects.count(),
        'stat_active': Statistic.objects.filter(is_active=True).count(),
        'initiative_count': Initiative.objects.count(),
        'initiative_active': Initiative.objects.filter(is_active=True).count(),
    }
    return render(request, 'cms/cms_dashboard.html', context)


# ─────────────────────────────────────────────────────────────
# BANNER CRUD
# ─────────────────────────────────────────────────────────────

@role_required('admin')
def banner_list_view(request):
    """List all banners ordered by display order."""
    banners = Banner.objects.all()
    return render(request, 'cms/banner_list.html', {'banners': banners})


@role_required('admin')
def banner_create_view(request):
    """Create a new banner."""
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Banner created successfully!')
            return redirect('cms:banner_list')
    else:
        form = BannerForm()
    return render(request, 'cms/banner_form.html', {
        'form': form,
        'form_title': 'Add New Banner',
        'submit_text': 'Create Banner',
    })


@role_required('admin')
def banner_edit_view(request, pk):
    """Edit an existing banner."""
    banner = get_object_or_404(Banner, pk=pk)
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES, instance=banner)
        if form.is_valid():
            form.save()
            messages.success(request, 'Banner updated successfully!')
            return redirect('cms:banner_list')
    else:
        form = BannerForm(instance=banner)
    return render(request, 'cms/banner_form.html', {
        'form': form,
        'form_title': 'Edit Banner',
        'submit_text': 'Save Changes',
        'object': banner,
    })


@role_required('admin')
def banner_delete_view(request, pk):
    """Delete a banner after confirmation."""
    banner = get_object_or_404(Banner, pk=pk)
    if request.method == 'POST':
        banner.delete()
        messages.success(request, 'Banner deleted successfully.')
        return redirect('cms:banner_list')
    return render(request, 'cms/confirm_delete.html', {
        'object': banner,
        'object_type': 'Banner',
        'cancel_url': 'cms:banner_list',
    })


# ─────────────────────────────────────────────────────────────
# VISION / MISSION CRUD
# ─────────────────────────────────────────────────────────────

@role_required('admin')
def vision_mission_list_view(request):
    """List all vision/mission items grouped by type."""
    items = VisionMission.objects.all()
    return render(request, 'cms/vision_mission_list.html', {'items': items})


@role_required('admin')
def vision_mission_create_view(request):
    """Create a new vision/mission item."""
    if request.method == 'POST':
        form = VisionMissionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vision/Mission item created successfully!')
            return redirect('cms:vision_mission_list')
    else:
        form = VisionMissionForm()
    return render(request, 'cms/vision_mission_form.html', {
        'form': form,
        'form_title': 'Add Vision / Mission Item',
        'submit_text': 'Create Item',
    })


@role_required('admin')
def vision_mission_edit_view(request, pk):
    """Edit an existing vision/mission item."""
    item = get_object_or_404(VisionMission, pk=pk)
    if request.method == 'POST':
        form = VisionMissionForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vision/Mission item updated successfully!')
            return redirect('cms:vision_mission_list')
    else:
        form = VisionMissionForm(instance=item)
    return render(request, 'cms/vision_mission_form.html', {
        'form': form,
        'form_title': 'Edit Vision / Mission Item',
        'submit_text': 'Save Changes',
        'object': item,
    })


@role_required('admin')
def vision_mission_delete_view(request, pk):
    """Delete a vision/mission item after confirmation."""
    item = get_object_or_404(VisionMission, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Vision/Mission item deleted successfully.')
        return redirect('cms:vision_mission_list')
    return render(request, 'cms/confirm_delete.html', {
        'object': item,
        'object_type': 'Vision / Mission Item',
        'cancel_url': 'cms:vision_mission_list',
    })


# ─────────────────────────────────────────────────────────────
# STATISTIC CRUD
# ─────────────────────────────────────────────────────────────

@role_required('admin')
def statistic_list_view(request):
    """List all impact statistics."""
    statistics = Statistic.objects.all()
    return render(request, 'cms/statistic_list.html', {'statistics': statistics})


@role_required('admin')
def statistic_create_view(request):
    """Create a new statistic."""
    if request.method == 'POST':
        form = StatisticForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Statistic created successfully!')
            return redirect('cms:statistic_list')
    else:
        form = StatisticForm()
    return render(request, 'cms/statistic_form.html', {
        'form': form,
        'form_title': 'Add New Statistic',
        'submit_text': 'Create Statistic',
    })


@role_required('admin')
def statistic_edit_view(request, pk):
    """Edit an existing statistic."""
    stat = get_object_or_404(Statistic, pk=pk)
    if request.method == 'POST':
        form = StatisticForm(request.POST, instance=stat)
        if form.is_valid():
            form.save()
            messages.success(request, 'Statistic updated successfully!')
            return redirect('cms:statistic_list')
    else:
        form = StatisticForm(instance=stat)
    return render(request, 'cms/statistic_form.html', {
        'form': form,
        'form_title': 'Edit Statistic',
        'submit_text': 'Save Changes',
        'object': stat,
    })


@role_required('admin')
def statistic_delete_view(request, pk):
    """Delete a statistic after confirmation."""
    stat = get_object_or_404(Statistic, pk=pk)
    if request.method == 'POST':
        stat.delete()
        messages.success(request, 'Statistic deleted successfully.')
        return redirect('cms:statistic_list')
    return render(request, 'cms/confirm_delete.html', {
        'object': stat,
        'object_type': 'Statistic',
        'cancel_url': 'cms:statistic_list',
    })


# ─────────────────────────────────────────────────────────────
# INITIATIVE CRUD
# ─────────────────────────────────────────────────────────────

@role_required('admin')
def initiative_list_view(request):
    """List all initiatives/programs."""
    initiatives = Initiative.objects.all()
    return render(request, 'cms/initiative_list.html', {'initiatives': initiatives})


@role_required('admin')
def initiative_create_view(request):
    """Create a new initiative."""
    if request.method == 'POST':
        form = InitiativeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Initiative created successfully!')
            return redirect('cms:initiative_list')
    else:
        form = InitiativeForm()
    return render(request, 'cms/initiative_form.html', {
        'form': form,
        'form_title': 'Add New Initiative',
        'submit_text': 'Create Initiative',
    })


@role_required('admin')
def initiative_edit_view(request, pk):
    """Edit an existing initiative."""
    initiative = get_object_or_404(Initiative, pk=pk)
    if request.method == 'POST':
        form = InitiativeForm(request.POST, request.FILES, instance=initiative)
        if form.is_valid():
            form.save()
            messages.success(request, 'Initiative updated successfully!')
            return redirect('cms:initiative_list')
    else:
        form = InitiativeForm(instance=initiative)
    return render(request, 'cms/initiative_form.html', {
        'form': form,
        'form_title': 'Edit Initiative',
        'submit_text': 'Save Changes',
        'object': initiative,
    })


@role_required('admin')
def initiative_delete_view(request, pk):
    """Delete an initiative after confirmation."""
    initiative = get_object_or_404(Initiative, pk=pk)
    if request.method == 'POST':
        initiative.delete()
        messages.success(request, 'Initiative deleted successfully.')
        return redirect('cms:initiative_list')
    return render(request, 'cms/confirm_delete.html', {
        'object': initiative,
        'object_type': 'Initiative',
        'cancel_url': 'cms:initiative_list',
    })
