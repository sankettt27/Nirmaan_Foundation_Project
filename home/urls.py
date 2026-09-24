"""
home/urls.py — URL patterns for the Home application.

URL map:
  /   → index (public landing page)
"""
from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about_view, name='about'),
    path('programs/', views.programs_view, name='programs'),
    path('impact/', views.impact_view, name='impact'),
    path('volunteer/', views.volunteer_view, name='volunteer'),
    path('partner/', views.partner_view, name='partner'),
    path('contact/', views.contact_view, name='contact'),
    path('projects/', views.projects_view, name='projects'),
    path('media/', views.media_view, name='media'),
]
