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
]
