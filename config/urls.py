"""
config/urls.py — Root URL Configuration for Nirmaan Foundation CMS
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django admin interface
    path('admin/', admin.site.urls),

    # Public-facing landing page (home app)
    path('', include('home.urls', namespace='home')),

    # All accounts-related URLs (login, register, dashboard, password reset)
    path('', include('accounts.urls', namespace='accounts')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
