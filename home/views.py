"""
home/views.py — Views for the public-facing Home (landing page) application.

Assignment 2 update: Now queries CMS models for dynamic content.
Falls back to static content if no CMS data exists.
"""
from django.shortcuts import redirect, render


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
        'has_vision_mission': vision_items.exists() or mission_items.exists(),
        'has_statistics': statistics.exists(),
        'has_initiatives': initiatives.exists(),
    }
    return render(request, 'home/index.html', context)


def about_view(request):
    """
    About Us page — Story, Mission & Vision, Core Values, Programs,
    Milestones Timeline, Leadership & Advisory Team, Impact and Events (Assignment 3).
    """
    from cms.models import (
        AboutEvent, AboutMilestone, TeamMember, VisionMission,
        OurStory, CoreValue, Program, Statistic
    )

    our_story = OurStory.objects.order_by('-updated_at').first()
    core_values = CoreValue.objects.filter(is_active=True).order_by('order', 'id')
    programs = Program.objects.filter(is_active=True).order_by('order', 'id')
    statistics = Statistic.objects.filter(is_active=True).order_by('order')

    milestones = AboutMilestone.objects.filter(is_active=True).order_by('order')
    team_members = TeamMember.objects.filter(is_active=True).order_by('order')
    leadership_team = team_members.filter(category='leadership')
    advisory_board = team_members.filter(category='advisory')
    chapter_leads = team_members.filter(category='chapter_lead')
    events = AboutEvent.objects.filter(is_active=True).order_by('order')
    vision_items = VisionMission.objects.filter(section_type='vision', is_active=True).order_by('order')
    mission_items = VisionMission.objects.filter(section_type='mission', is_active=True).order_by('order')

    context = {
        'page_title': 'About Us — Our Story, Values & Leadership',
        'active_nav': 'about',
        'our_story': our_story,
        'has_story': bool(our_story and our_story.content),
        'core_values': core_values,
        'has_core_values': core_values.exists(),
        'programs': programs,
        'has_programs': programs.exists(),
        'statistics': statistics,
        'has_statistics': statistics.exists(),
        'milestones': milestones,
        'has_milestones': milestones.exists(),
        'team_members': team_members,
        'leadership_team': leadership_team,
        'advisory_board': advisory_board,
        'chapter_leads': chapter_leads,
        'has_team': team_members.exists(),
        'events': events,
        'has_events': events.exists(),
        'vision_items': vision_items,
        'mission_items': mission_items,
        'has_vision_mission': vision_items.exists() or mission_items.exists(),
    }
    return render(request, 'home/about.html', context)


def programs_view(request):
    """
    Programs page — Flagship educational initiatives, curriculum highlights,
    beneficiaries reached, and volunteer matching.
    """
    from cms.models import FAQ, Initiative, Statistic

    programs = Initiative.objects.filter(is_active=True).order_by('order')
    statistics = Statistic.objects.filter(is_active=True).order_by('order')
    faqs = FAQ.objects.filter(category__in=['programs', 'general'], is_active=True).order_by('order')

    context = {
        'page_title': 'Our Programs — Educational & Holistic Development Initiatives',
        'active_nav': 'programs',
        'programs': programs,
        'has_programs': programs.exists(),
        'statistics': statistics,
        'faqs': faqs,
    }
    return render(request, 'home/programs.html', context)


def impact_view(request):
    """
    Impact page — Decadal metrics, student & community case studies,
    audited annual reports, and governance disclosures.
    """
    from cms.models import AnnualReport, ImpactStory, Statistic

    statistics = Statistic.objects.filter(is_active=True).order_by('order')
    stories = ImpactStory.objects.filter(is_active=True).order_by('order')
    reports = AnnualReport.objects.filter(is_active=True).order_by('order')

    context = {
        'page_title': 'Our Impact — 10+ Years of Measurable Social Transformation',
        'active_nav': 'impact',
        'statistics': statistics,
        'stories': stories,
        'has_stories': stories.exists(),
        'reports': reports,
        'has_reports': reports.exists(),
    }
    return render(request, 'home/impact.html', context)


def volunteer_view(request):
    """
    Volunteer page — Why volunteer, 4-step volunteer journey,
    available teaching & mentoring roles, FAQs, and registration CTA.
    """
    from cms.models import FAQ, Statistic, VolunteerOpportunity

    opportunities = VolunteerOpportunity.objects.filter(is_active=True).order_by('order')
    statistics = Statistic.objects.filter(is_active=True).order_by('order')
    faqs = FAQ.objects.filter(category='volunteer', is_active=True).order_by('order')

    context = {
        'page_title': 'Volunteer With Us — Join India\'s Youth Volunteer Movement',
        'active_nav': 'volunteer',
        'opportunities': opportunities,
        'has_opportunities': opportunities.exists(),
        'statistics': statistics,
        'faqs': faqs,
    }
    return render(request, 'home/volunteer.html', context)


def partner_view(request):
    """
    Partner With Us page — Corporate CSR collaborations, institutional grants,
    tax exemptions (80G & 12A), school adoption models, and partner logos.
    """
    from cms.models import FAQ, PartnerOrganization

    partners = PartnerOrganization.objects.filter(is_active=True).order_by('order')
    faqs = FAQ.objects.filter(category='partner', is_active=True).order_by('order')

    context = {
        'page_title': 'Partner With Us — High-Impact CSR & Institutional Alliances',
        'active_nav': 'partner',
        'partners': partners,
        'has_partners': partners.exists(),
        'faqs': faqs,
    }
    return render(request, 'home/partner.html', context)


def contact_view(request):
    """
    Contact Us page — Chapter offices, interactive inquiry form,
    FAQ accordion, and general support channels.
    """
    from django.contrib import messages
    from cms.models import ContactInquiry, FAQ, OfficeLocation

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        category = request.POST.get('category', 'general')
        subject = request.POST.get('subject', '').strip()
        message_text = request.POST.get('message', '').strip()

        if name and email and message_text:
            ContactInquiry.objects.create(
                name=name,
                email=email,
                phone=phone,
                category=category,
                subject=subject or f'Inquiry from {name}',
                message=message_text,
            )
            messages.success(request, 'Thank you for reaching out! Your message has been received and our team will get back to you within 24–48 hours.')
            return redirect('home:contact')
        else:
            messages.error(request, 'Please provide your name, email, and message.')

    offices = OfficeLocation.objects.filter(is_active=True).order_by('order')
    faqs = FAQ.objects.filter(is_active=True).order_by('order')

    context = {
        'page_title': 'Contact Us — Get in Touch with Nirmaan Foundation',
        'active_nav': 'contact',
        'offices': offices,
        'has_offices': offices.exists(),
        'faqs': faqs,
    }
    return render(request, 'home/contact.html', context)


def projects_view(request):
    """
    Projects page — dynamic project showcase with filtering by status.
    """
    from cms.models import Project

    status_filter = request.GET.get('status')
    
    if status_filter and status_filter in ['Ongoing', 'Completed', 'Upcoming']:
        projects = Project.objects.filter(status=status_filter).order_by('-start_date')
    else:
        projects = Project.objects.all().order_by('-start_date')

    context = {
        'page_title': 'Our Projects — Building a Better Future',
        'active_nav': 'projects',
        'projects': projects,
        'has_projects': projects.exists(),
        'current_status': status_filter or 'All',
    }
    return render(request, 'home/projects.html', context)


def media_view(request):
    """
    Media page — Press releases, coverage, gallery, and videos.
    """
    from cms.models import PressRelease, MediaCoverage, ImageGallery, Video

    context = {
        'page_title': 'Media Room — News and Updates',
        'active_nav': 'media',
        'press_releases': PressRelease.objects.all()[:5],
        'media_coverage': MediaCoverage.objects.all()[:10],
        'gallery_images': ImageGallery.objects.all()[:12],
        'videos': Video.objects.all()[:6],
    }
    return render(request, 'home/media.html', context)
