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
]
