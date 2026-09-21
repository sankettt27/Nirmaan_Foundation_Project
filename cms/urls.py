"""
cms/urls.py — URL patterns for the CMS application.

All routes are under /dashboard/admin/home/ and are admin-only.

URL map:
  /dashboard/admin/home/                        → CMS Dashboard
  /dashboard/admin/home/banners/                → Banner list
  /dashboard/admin/home/banners/add/            → Banner create
  /dashboard/admin/home/banners/<id>/edit/       → Banner edit
  /dashboard/admin/home/banners/<id>/delete/     → Banner delete
  (same pattern for vision-mission/, statistics/, initiatives/)
"""

from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [
    # ── CMS Dashboard ─────────────────────────────────────────
    path('dashboard/admin/home/', views.cms_dashboard_view, name='cms_dashboard'),

    # ── Banners ───────────────────────────────────────────────
    path('dashboard/admin/home/banners/', views.banner_list_view, name='banner_list'),
    path('dashboard/admin/home/banners/add/', views.banner_create_view, name='banner_create'),
    path('dashboard/admin/home/banners/<int:pk>/edit/', views.banner_edit_view, name='banner_edit'),
    path('dashboard/admin/home/banners/<int:pk>/delete/', views.banner_delete_view, name='banner_delete'),

    # ── Vision / Mission ──────────────────────────────────────
    path('dashboard/admin/home/vision-mission/', views.vision_mission_list_view, name='vision_mission_list'),
    path('dashboard/admin/home/vision-mission/add/', views.vision_mission_create_view, name='vision_mission_create'),
    path('dashboard/admin/home/vision-mission/<int:pk>/edit/', views.vision_mission_edit_view, name='vision_mission_edit'),
    path('dashboard/admin/home/vision-mission/<int:pk>/delete/', views.vision_mission_delete_view, name='vision_mission_delete'),

    # ── Statistics ────────────────────────────────────────────
    path('dashboard/admin/home/statistics/', views.statistic_list_view, name='statistic_list'),
    path('dashboard/admin/home/statistics/add/', views.statistic_create_view, name='statistic_create'),
    path('dashboard/admin/home/statistics/<int:pk>/edit/', views.statistic_edit_view, name='statistic_edit'),
    path('dashboard/admin/home/statistics/<int:pk>/delete/', views.statistic_delete_view, name='statistic_delete'),

    # ── Initiatives ───────────────────────────────────────────
    path('dashboard/admin/home/initiatives/', views.initiative_list_view, name='initiative_list'),
    path('dashboard/admin/home/initiatives/add/', views.initiative_create_view, name='initiative_create'),
    path('dashboard/admin/home/initiatives/<int:pk>/edit/', views.initiative_edit_view, name='initiative_edit'),
    path('dashboard/admin/home/initiatives/<int:pk>/delete/', views.initiative_delete_view, name='initiative_delete'),

    # ── Events & Activities (About Page) ──────────────────────
    path('dashboard/admin/events/', views.event_list_view, name='event_list'),
    path('dashboard/admin/events/add/', views.event_create_view, name='event_create'),
    path('dashboard/admin/events/<int:pk>/edit/', views.event_edit_view, name='event_edit'),
    path('dashboard/admin/events/<int:pk>/delete/', views.event_delete_view, name='event_delete'),

    # ── Team & Leadership (About Page) ────────────────────────
    path('dashboard/admin/team/', views.team_list_view, name='team_list'),
    path('dashboard/admin/team/add/', views.team_create_view, name='team_create'),
    path('dashboard/admin/team/<int:pk>/edit/', views.team_edit_view, name='team_edit'),
    path('dashboard/admin/team/<int:pk>/delete/', views.team_delete_view, name='team_delete'),

    # ── Milestones Timeline (About Page) ──────────────────────
    path('dashboard/admin/milestones/', views.milestone_list_view, name='milestone_list'),
    path('dashboard/admin/milestones/add/', views.milestone_create_view, name='milestone_create'),
    path('dashboard/admin/milestones/<int:pk>/edit/', views.milestone_edit_view, name='milestone_edit'),
    path('dashboard/admin/milestones/<int:pk>/delete/', views.milestone_delete_view, name='milestone_delete'),

    # ── Impact Stories (Impact Page) ──────────────────────────
    path('dashboard/admin/stories/', views.story_list_view, name='story_list'),
    path('dashboard/admin/stories/add/', views.story_create_view, name='story_create'),
    path('dashboard/admin/stories/<int:pk>/edit/', views.story_edit_view, name='story_edit'),
    path('dashboard/admin/stories/<int:pk>/delete/', views.story_delete_view, name='story_delete'),

    # ── Annual Reports (Impact Page) ──────────────────────────
    path('dashboard/admin/reports/', views.report_list_view, name='report_list'),
    path('dashboard/admin/reports/add/', views.report_create_view, name='report_create'),
    path('dashboard/admin/reports/<int:pk>/edit/', views.report_edit_view, name='report_edit'),
    path('dashboard/admin/reports/<int:pk>/delete/', views.report_delete_view, name='report_delete'),

    # ── Volunteer Opportunities (Volunteer Page) ──────────────
    path('dashboard/admin/opportunities/', views.opportunity_list_view, name='opportunity_list'),
    path('dashboard/admin/opportunities/add/', views.opportunity_create_view, name='opportunity_create'),
    path('dashboard/admin/opportunities/<int:pk>/edit/', views.opportunity_edit_view, name='opportunity_edit'),
    path('dashboard/admin/opportunities/<int:pk>/delete/', views.opportunity_delete_view, name='opportunity_delete'),

    # ── Partner Organizations (Partner Page) ──────────────────
    path('dashboard/admin/partners/', views.partner_list_view, name='partner_list'),
    path('dashboard/admin/partners/add/', views.partner_create_view, name='partner_create'),
    path('dashboard/admin/partners/<int:pk>/edit/', views.partner_edit_view, name='partner_edit'),
    path('dashboard/admin/partners/<int:pk>/delete/', views.partner_delete_view, name='partner_delete'),

    # ── Chapter Offices (Contact Page) ────────────────────────
    path('dashboard/admin/offices/', views.office_list_view, name='office_list'),
    path('dashboard/admin/offices/add/', views.office_create_view, name='office_create'),
    path('dashboard/admin/offices/<int:pk>/edit/', views.office_edit_view, name='office_edit'),
    path('dashboard/admin/offices/<int:pk>/delete/', views.office_delete_view, name='office_delete'),

    # ── FAQs (Categorized) ────────────────────────────────────
    path('dashboard/admin/faqs/', views.faq_list_view, name='faq_list'),
    path('dashboard/admin/faqs/add/', views.faq_create_view, name='faq_create'),
    path('dashboard/admin/faqs/<int:pk>/edit/', views.faq_edit_view, name='faq_edit'),
    path('dashboard/admin/faqs/<int:pk>/delete/', views.faq_delete_view, name='faq_delete'),

    # ── Contact Inquiries ─────────────────────────────────────
    path('dashboard/admin/inquiries/', views.inquiry_list_view, name='inquiry_list'),
    path('dashboard/admin/inquiries/<int:pk>/toggle-resolved/', views.inquiry_toggle_resolved_view, name='inquiry_toggle_resolved'),
    path('dashboard/admin/inquiries/<int:pk>/delete/', views.inquiry_delete_view, name='inquiry_delete'),
]

