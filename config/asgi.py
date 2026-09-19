"""
config/asgi.py — ASGI entry point for Nirmaan Foundation CMS.
Used by ASGI servers such as Uvicorn/Daphne for async support.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()
