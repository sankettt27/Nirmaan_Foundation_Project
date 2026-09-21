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
from django.urls import reverse

from accounts.views import role_required

from .forms import (
    BannerForm, InitiativeForm, StatisticForm, VisionMissionForm,
    AboutMilestoneForm, TeamMemberForm, AboutEventForm,
    ImpactStoryForm, AnnualReportForm, VolunteerOpportunityForm,
    PartnerOrganizationForm, OfficeLocationForm, FAQForm
)
from .models import (
    Banner, Initiative, Statistic, VisionMission,
    AboutMilestone, TeamMember, AboutEvent,
    ImpactStory, AnnualReport, VolunteerOpportunity,
    PartnerOrganization, OfficeLocation, FAQ, ContactInquiry
)


# ─────────────────────────────────────────────────────────────
# CMS DASHBOARD — OVERVIEW
# ─────────────────────────────────────────────────────────────

@role_required('admin')
def cms_dashboard_view(request):
    """
    CMS Overview page — shows counts of all content items across all pages
    with quick links for each section.
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
        # New page models
        'milestone_count': AboutMilestone.objects.count(),
        'milestone_active': AboutMilestone.objects.filter(is_active=True).count(),
        'team_count': TeamMember.objects.count(),
        'team_active': TeamMember.objects.filter(is_active=True).count(),
        'event_count': AboutEvent.objects.count(),
        'event_active': AboutEvent.objects.filter(is_active=True).count(),
        'story_count': ImpactStory.objects.count(),
        'story_active': ImpactStory.objects.filter(is_active=True).count(),
        'report_count': AnnualReport.objects.count(),
        'report_active': AnnualReport.objects.filter(is_active=True).count(),
        'opportunity_count': VolunteerOpportunity.objects.count(),
        'opportunity_active': VolunteerOpportunity.objects.filter(is_active=True).count(),
        'partner_count': PartnerOrganization.objects.count(),
        'partner_active': PartnerOrganization.objects.filter(is_active=True).count(),
        'office_count': OfficeLocation.objects.count(),
        'office_active': OfficeLocation.objects.filter(is_active=True).count(),
        'faq_count': FAQ.objects.count(),
        'faq_active': FAQ.objects.filter(is_active=True).count(),
        'inquiry_count': ContactInquiry.objects.count(),
        'inquiry_pending': ContactInquiry.objects.filter(is_resolved=False).count(),
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


# ─────────────────────────────────────────────────────────────
# ABOUT EVENTS & ACTIVITIES CRUD
# ─────────────────────────────────────────────────────────────

@role_required('admin')
def event_list_view(request):
    events = AboutEvent.objects.all().order_by('order')
    return render(request, 'cms/events_list.html', {'events': events})


@role_required('admin')
def event_create_view(request):
    if request.method == 'POST':
        form = AboutEventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event created successfully!')
            return redirect('cms:event_list')
    else:
        form = AboutEventForm()
    return render(request, 'cms/generic_form.html', {
        'form': form,
        'form_title': 'Add Event / Activity',
        'form_subtitle': 'Add an event, science mela, or field workshop with photos for the About page',
        'submit_text': 'Create Event',
        'back_url': reverse('cms:event_list'),
        'active_cms': 'events',
    })


@role_required('admin')
def event_edit_view(request, pk):
    event = get_object_or_404(AboutEvent, pk=pk)
    if request.method == 'POST':
        form = AboutEventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('cms:event_list')
    else:
        form = AboutEventForm(instance=event)
    return render(request, 'cms/generic_form.html', {
        'form': form,
        'form_title': 'Edit Event',
        'form_subtitle': 'Update event details, photos, or description',
        'submit_text': 'Save Changes',
        'object': event,
        'back_url': reverse('cms:event_list'),
        'active_cms': 'events',
    })


@role_required('admin')
def event_delete_view(request, pk):
    event = get_object_or_404(AboutEvent, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully.')
        return redirect('cms:event_list')
    return render(request, 'cms/confirm_delete.html', {
        'object': event,
        'object_type': 'Event',
        'cancel_url': 'cms:event_list',
    })


# ─────────────────────────────────────────────────────────────
# TEAM MEMBERS & LEADERSHIP CRUD
# ─────────────────────────────────────────────────────────────

@role_required('admin')
def team_list_view(request):
    team_members = TeamMember.objects.all().order_by('order')
    return render(request, 'cms/team_list.html', {'team_members': team_members})


@role_required('admin')
def team_create_view(request):
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team member added successfully!')
            return redirect('cms:team_list')
    else:
        form = TeamMemberForm()
    return render(request, 'cms/generic_form.html', {
        'form': form,
        'form_title': 'Add Team Member',
        'form_subtitle': 'Add a trustee, executive leader, advisor, or chapter coordinator',
        'submit_text': 'Add Member',
        'back_url': reverse('cms:team_list'),
        'active_cms': 'team',
    })


@role_required('admin')
def team_edit_view(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team member updated successfully!')
            return redirect('cms:team_list')
    else:
        form = TeamMemberForm(instance=member)
    return render(request, 'cms/generic_form.html', {
        'form': form,
        'form_title': 'Edit Team Member',
        'submit_text': 'Save Changes',
        'object': member,
        'back_url': reverse('cms:team_list'),
        'active_cms': 'team',
    })


@role_required('admin')
def team_delete_view(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    if request.method == 'POST':
        member.delete()
        messages.success(request, 'Team member deleted successfully.')
        return redirect('cms:team_list')
    return render(request, 'cms/confirm_delete.html', {
        'object': member,
        'object_type': 'Team Member',
        'cancel_url': 'cms:team_list',
    })


# ─────────────────────────────────────────────────────────────
# MILESTONES TIMELINE CRUD
# ─────────────────────────────────────────────────────────────

@role_required('admin')
def milestone_list_view(request):
    milestones = AboutMilestone.objects.all().order_by('order')
    return render(request, 'cms/milestones_list.html', {'milestones': milestones})


@role_required('admin')
def milestone_create_view(request):
    if request.method == 'POST':
        form = AboutMilestoneForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Milestone added successfully!')
            return redirect('cms:milestone_list')
    else:
        form = AboutMilestoneForm()
    return render(request, 'cms/generic_form.html', {
        'form': form,
        'form_title': 'Add Milestone',
        'form_subtitle': 'Add a founding year or historical expansion milestone to the journey timeline',
        'submit_text': 'Add Milestone',
        'back_url': reverse('cms:milestone_list'),
        'active_cms': 'milestones',
    })


@role_required('admin')
def milestone_edit_view(request, pk):
    milestone = get_object_or_404(AboutMilestone, pk=pk)
    if request.method == 'POST':
        form = AboutMilestoneForm(request.POST, instance=milestone)
        if form.is_valid():
            form.save()
            messages.success(request, 'Milestone updated successfully!')
            return redirect('cms:milestone_list')
    else:
        form = AboutMilestoneForm(instance=milestone)
    return render(request, 'cms/generic_form.html', {
        'form': form,
        'form_title': 'Edit Milestone',
        'submit_text': 'Save Changes',
        'object': milestone,
        'back_url': reverse('cms:milestone_list'),
        'active_cms': 'milestones',
    })


@role_required('admin')
def milestone_delete_view(request, pk):
    milestone = get_object_or_404(AboutMilestone, pk=pk)
    if request.method == 'POST':
        milestone.delete()
        messages.success(request, 'Milestone deleted successfully.')
        return redirect('cms:milestone_list')
    return render(request, 'cms/confirm_delete.html', {
        'object': milestone,
        'object_type': 'Milestone',
        'cancel_url': 'cms:milestone_list',
    })


# ─────────────────────────────────────────────────────────────
# IMPACT STORIES CRUD
# ─────────────────────────────────────────────────────────────

@role_required('admin')
def story_list_view(request):
    stories = ImpactStory.objects.all().order_by('order')
    return render(request, 'cms/stories_list.html', {'stories': stories})


@role_required('admin')
def story_create_view(request):
    if request.method == 'POST':
        form = ImpactStoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Impact story added successfully!')
            return redirect('cms:story_list')
    else:
        form = ImpactStoryForm()
    return render(request, 'cms/generic_form.html', {
        'form': form,
        'form_title': 'Add Impact Story',
        'form_subtitle': 'Add a student, teacher, or volunteer transformation case study',
        'submit_text': 'Publish Story',
        'back_url': reverse('cms:story_list'),
        'active_cms': 'stories',
    })


@role_required('admin')
def story_edit_view(request, pk):
    story = get_object_or_404(ImpactStory, pk=pk)
    if request.method == 'POST':
        form = ImpactStoryForm(request.POST, request.FILES, instance=story)
        if form.is_valid():
            form.save()
            messages.success(request, 'Impact story updated successfully!')
            return redirect('cms:story_list')
    else:
        form = ImpactStoryForm(instance=story)
    return render(request, 'cms/generic_form.html', {
        'form': form,
        'form_title': 'Edit Impact Story',
        'submit_text': 'Save Changes',
        'object': story,
        'back_url': reverse('cms:story_list'),
        'active_cms': 'stories',
    })


@role_required('admin')
def story_delete_view(request, pk):
    story = get_object_or_404(ImpactStory, pk=pk)
    if request.method == 'POST':
        story.delete()
        messages.success(request, 'Impact story deleted successfully.')
        return redirect('cms:story_list')
    return render(request, 'cms/confirm_delete.html', {
        'object': story,
        'object_type': 'Impact Story',
        'cancel_url': 'cms:story_list',
    })


# ─────────────────────────────────────────────────────────────
# ANNUAL REPORTS CRUD
# ─────────────────────────────────────────────────────────────

@role_required('admin')
def report_list_view(request):
    reports = AnnualReport.objects.all().order_by('order')
    return render(request, 'cms/reports_list.html', {'reports': reports})


@role_required('admin')
def report_create_view(request):
    if request.method == 'POST':
        form = AnnualReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Annual report added successfully!')
            return redirect('cms:report_list')
    else:
        form = AnnualReportForm()
    return render(request, 'cms/generic_form.html', {
        'form': form,
        'form_title': 'Add Annual Report',
        'form_subtitle': 'Upload or link audited statements and fiscal disclosures',
        'submit_text': 'Add Report',
        'back_url': reverse('cms:report_list'),
        'active_cms': 'reports',
    })


@role_required('admin')
def report_edit_view(request, pk):
    report = get_object_or_404(AnnualReport, pk=pk)
    if request.method == 'POST':
        form = AnnualReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, 'Annual report updated successfully!')
            return redirect('cms:report_list')
    else:
        form = AnnualReportForm(instance=report)
    return render(request, 'cms/generic_form.html', {
        'form': form,
        'form_title': 'Edit Annual Report',
        'submit_text': 'Save Changes',
        'object': report,
        'back_url': reverse('cms:report_list'),
        'active_cms': 'reports',
    })


@role_required('admin')
def report_delete_view(request, pk):
    report = get_object_or_404(AnnualReport, pk=pk)
    if request.method == 'POST':
        report.delete()
        messages.success(request, 'Annual report deleted successfully.')
        return redirect('cms:report_list')
    return render(request, 'cms/confirm_delete.html', {
        'object': report,
        'object_type': 'Annual Report',
        'cancel_url': 'cms:report_list',
    })


# ─────────────────────────────────────────────────────────────
# VOLUNTEER OPPORTUNITIES CRUD
# ─────────────────────────────────────────────────────────────

@role_required('admin')
def opportunity_list_view(request):
    opportunities = VolunteerOpportunity.objects.all().order_by('order')
    return render(request, 'cms/opportunities_list.html', {'opportunities': opportunities})


@role_required('admin')
def opportunity_create_view(request):
    if request.method == 'POST':
        form = VolunteerOpportunityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Volunteer role created successfully!')
            return redirect('cms:opportunity_list')
    else:
        form = VolunteerOpportunityForm()
    return render(request, 'cms/generic_form.html', {
        'form': form,
        'form_title': 'Add Volunteer Opportunity',
        'form_subtitle': 'List an open teaching, mentoring, or operations volunteering role',
        'submit_text': 'Publish Role',
        'back_url': reverse('cms:opportunity_list'),
        'active_cms': 'opportunities',
    })


@role_required('admin')
def opportunity_edit_view(request, pk):
    opp = get_object_or_404(VolunteerOpportunity, pk=pk)
    if request.method == 'POST':
        form = VolunteerOpportunityForm(request.POST, instance=opp)
        if form.is_valid():
            form.save()
            messages.success(request, 'Volunteer role updated successfully!')
            return redirect('cms:opportunity_list')
    else:
        form = VolunteerOpportunityForm(instance=opp)
    return render(request, 'cms/generic_form.html', {
        'form': form,
        'form_title': 'Edit Volunteer Opportunity',
        'submit_text': 'Save Changes',
        'object': opp,
        'back_url': reverse('cms:opportunity_list'),
        'active_cms': 'opportunities',
    })


@role_required('admin')
def opportunity_delete_view(request, pk):
    opp = get_object_or_404(VolunteerOpportunity, pk=pk)
    if request.method == 'POST':
        opp.delete()
        messages.success(request, 'Volunteer role deleted successfully.')
        return redirect('cms:opportunity_list')
    return render(request, 'cms/confirm_delete.html', {
        'object': opp,
        'object_type': 'Volunteer Opportunity',
        'cancel_url': 'cms:opportunity_list',
    })


# ─────────────────────────────────────────────────────────────
# PARTNER ORGANIZATIONS CRUD
# ─────────────────────────────────────────────────────────────

@role_required('admin')
def partner_list_view(request):
    partners = PartnerOrganization.objects.all().order_by('order')
    return render(request, 'cms/partners_list.html', {'partners': partners})


@role_required('admin')
def partner_create_view(request):
    if request.method == 'POST':
        form = PartnerOrganizationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Partner organization added successfully!')
            return redirect('cms:partner_list')
    else:
        form = PartnerOrganizationForm()
    return render(request, 'cms/generic_form.html', {
        'form': form,
        'form_title': 'Add Partner Organization',
        'form_subtitle': 'Add a corporate CSR partner, institutional grantor, or school network',
        'submit_text': 'Add Partner',
        'back_url': reverse('cms:partner_list'),
        'active_cms': 'partners',
    })


@role_required('admin')
def partner_edit_view(request, pk):
    partner = get_object_or_404(PartnerOrganization, pk=pk)
    if request.method == 'POST':
        form = PartnerOrganizationForm(request.POST, request.FILES, instance=partner)
        if form.is_valid():
            form.save()
            messages.success(request, 'Partner organization updated successfully!')
            return redirect('cms:partner_list')
    else:
        form = PartnerOrganizationForm(instance=partner)
    return render(request, 'cms/generic_form.html', {
        'form': form,
        'form_title': 'Edit Partner Organization',
        'submit_text': 'Save Changes',
        'object': partner,
        'back_url': reverse('cms:partner_list'),
        'active_cms': 'partners',
    })


@role_required('admin')
def partner_delete_view(request, pk):
    partner = get_object_or_404(PartnerOrganization, pk=pk)
    if request.method == 'POST':
        partner.delete()
        messages.success(request, 'Partner organization deleted successfully.')
        return redirect('cms:partner_list')
    return render(request, 'cms/confirm_delete.html', {
        'object': partner,
        'object_type': 'Partner Organization',
        'cancel_url': 'cms:partner_list',
    })


# ─────────────────────────────────────────────────────────────
# CHAPTER OFFICES CRUD
# ─────────────────────────────────────────────────────────────

@role_required('admin')
def office_list_view(request):
    offices = OfficeLocation.objects.all().order_by('order')
    return render(request, 'cms/offices_list.html', {'offices': offices})


@role_required('admin')
def office_create_view(request):
    if request.method == 'POST':
        form = OfficeLocationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Chapter office added successfully!')
            return redirect('cms:office_list')
    else:
        form = OfficeLocationForm()
    return render(request, 'cms/generic_form.html', {
        'form': form,
        'form_title': 'Add Chapter Office',
        'form_subtitle': 'Add a national HQ or city chapter address and contact info',
        'submit_text': 'Add Office',
        'back_url': reverse('cms:office_list'),
        'active_cms': 'offices',
    })


@role_required('admin')
def office_edit_view(request, pk):
    office = get_object_or_404(OfficeLocation, pk=pk)
    if request.method == 'POST':
        form = OfficeLocationForm(request.POST, instance=office)
        if form.is_valid():
            form.save()
            messages.success(request, 'Chapter office updated successfully!')
            return redirect('cms:office_list')
    else:
        form = OfficeLocationForm(instance=office)
    return render(request, 'cms/generic_form.html', {
        'form': form,
        'form_title': 'Edit Chapter Office',
        'submit_text': 'Save Changes',
        'object': office,
        'back_url': reverse('cms:office_list'),
        'active_cms': 'offices',
    })


@role_required('admin')
def office_delete_view(request, pk):
    office = get_object_or_404(OfficeLocation, pk=pk)
    if request.method == 'POST':
        office.delete()
        messages.success(request, 'Chapter office deleted successfully.')
        return redirect('cms:office_list')
    return render(request, 'cms/confirm_delete.html', {
        'object': office,
        'object_type': 'Office Location',
        'cancel_url': 'cms:office_list',
    })


# ─────────────────────────────────────────────────────────────
# FAQS CRUD
# ─────────────────────────────────────────────────────────────

@role_required('admin')
def faq_list_view(request):
    faqs = FAQ.objects.all().order_by('order')
    return render(request, 'cms/faqs_list.html', {'faqs': faqs})


@role_required('admin')
def faq_create_view(request):
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'FAQ added successfully!')
            return redirect('cms:faq_list')
    else:
        form = FAQForm()
    return render(request, 'cms/generic_form.html', {
        'form': form,
        'form_title': 'Add FAQ Question',
        'form_subtitle': 'Add a question and answer for volunteers, programs, or partners',
        'submit_text': 'Add FAQ',
        'back_url': reverse('cms:faq_list'),
        'active_cms': 'faqs',
    })


@role_required('admin')
def faq_edit_view(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    if request.method == 'POST':
        form = FAQForm(request.POST, instance=faq)
        if form.is_valid():
            form.save()
            messages.success(request, 'FAQ updated successfully!')
            return redirect('cms:faq_list')
    else:
        form = FAQForm(instance=faq)
    return render(request, 'cms/generic_form.html', {
        'form': form,
        'form_title': 'Edit FAQ',
        'submit_text': 'Save Changes',
        'object': faq,
        'back_url': reverse('cms:faq_list'),
        'active_cms': 'faqs',
    })


@role_required('admin')
def faq_delete_view(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    if request.method == 'POST':
        faq.delete()
        messages.success(request, 'FAQ deleted successfully.')
        return redirect('cms:faq_list')
    return render(request, 'cms/confirm_delete.html', {
        'object': faq,
        'object_type': 'FAQ',
        'cancel_url': 'cms:faq_list',
    })


# ─────────────────────────────────────────────────────────────
# CONTACT INQUIRIES MANAGEMENT
# ─────────────────────────────────────────────────────────────

@role_required('admin')
def inquiry_list_view(request):
    inquiries = ContactInquiry.objects.all().order_by('-created_at')
    return render(request, 'cms/inquiries_list.html', {'inquiries': inquiries})


@role_required('admin')
def inquiry_toggle_resolved_view(request, pk):
    inquiry = get_object_or_404(ContactInquiry, pk=pk)
    inquiry.is_resolved = not inquiry.is_resolved
    inquiry.save()
    messages.success(request, f'Inquiry status updated to {"Resolved" if inquiry.is_resolved else "Pending"}.')
    return redirect('cms:inquiry_list')


@role_required('admin')
def inquiry_delete_view(request, pk):
    inquiry = get_object_or_404(ContactInquiry, pk=pk)
    if request.method == 'POST':
        inquiry.delete()
        messages.success(request, 'Inquiry deleted successfully.')
        return redirect('cms:inquiry_list')
    return render(request, 'cms/confirm_delete.html', {
        'object': f"Inquiry from {inquiry.name} ({inquiry.subject})",
        'object_type': 'Contact Inquiry',
        'cancel_url': 'cms:inquiry_list',
    })

