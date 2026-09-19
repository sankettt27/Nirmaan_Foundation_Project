"""
home/apps.py — App configuration for the Home (public landing page) application.
"""
from django.apps import AppConfig


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'
    verbose_name = 'Home'
