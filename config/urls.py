"""
config/urls.py — Root URL Configuration for Nirmaan Foundation CMS
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.http import HttpResponse

urlpatterns = [
    # Lightweight health check endpoint (keeps Render alive via external pinger)
    path('health/', lambda request: HttpResponse("OK", content_type="text/plain"), name='health'),

    # Django admin interface
    path('admin/', admin.site.urls),

    # Public-facing landing page (home app)
    path('', include('home.urls', namespace='home')),

    # All accounts-related URLs (login, register, dashboard, password reset)
    path('', include('accounts.urls', namespace='accounts')),

    # CMS — Home Page Content Management (admin-only)
    path('', include('cms.urls', namespace='cms')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
