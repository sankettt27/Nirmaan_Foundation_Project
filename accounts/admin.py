"""
accounts/admin.py — Django Admin configuration for the Accounts app.

Registers CustomUser in Django Admin so administrators can:
  - View and search all users
  - Change user status (active / inactive)
  - Change user roles
  - Reset passwords securely
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin interface for CustomUser model."""

    # Columns shown in the user list view
    list_display = ('email', 'full_name', 'role', 'status', 'is_staff', 'created_at')
    list_filter = ('role', 'status', 'is_staff', 'is_superuser')
    search_fields = ('email', 'full_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    # Fields shown when editing an existing user
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Information'), {'fields': ('full_name',)}),
        (_('Role & Status'), {'fields': ('role', 'status')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Timestamps'), {'fields': ('created_at', 'last_login')}),
    )

    # Fields shown when creating a new user via admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'role', 'status', 'password1', 'password2'),
        }),
    )


from .models import PasswordResetOTP


@admin.register(PasswordResetOTP)
class PasswordResetOTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'expires_at', 'is_used', 'attempts')
    list_filter = ('is_used', 'created_at')
    search_fields = ('user__email', 'user__full_name')
    readonly_fields = ('user', 'otp_hash', 'created_at', 'expires_at', 'attempts')

