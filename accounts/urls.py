"""
accounts/urls.py — URL patterns for the Accounts application.

URL map:
  /login/                                      → login_view
  /logout/                                     → logout_view
  /register/                                   → register_view
  /dashboard/admin/                            → admin_dashboard_view
  /dashboard/user/                             → user_dashboard_view
  /password-reset/                             → PasswordResetView (Django built-in)
  /password-reset/done/                        → PasswordResetDoneView
  /password-reset/confirm/<uidb64>/<token>/    → PasswordResetConfirmView
  /password-reset/complete/                    → PasswordResetCompleteView

Password reset uses Django's built-in signed-token mechanism.
Custom templates are used for brand consistency.
"""

from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    # ── Authentication ────────────────────────────────────────
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # ── Dashboards ────────────────────────────────────────────
    path('dashboard/admin/', views.admin_dashboard_view, name='admin_dashboard'),
    path('dashboard/volunteer/', views.volunteer_dashboard_view, name='volunteer_dashboard'),
    path('dashboard/donor/', views.donor_dashboard_view, name='donor_dashboard'),

    # ── Password Reset (OTP-Based) ───────────────────────────
    path(
        'password-reset/',
        views.password_reset_request_view,
        name='password_reset',
    ),
    path(
        'password-reset/verify/',
        views.password_reset_verify_view,
        name='password_reset_verify',
    ),
    path(
        'password-reset/resend/',
        views.password_reset_resend_view,
        name='password_reset_resend',
    ),
]
