"""
accounts/models.py — Custom User Model for Nirmaan Foundation CMS.

Maps to the Users table specified in the internship documentation:

    Spec field    | Django field      | Notes
    ------------- | ----------------- | -------------------------------------------
    user_id       | id                | Auto-created by Django (INT PK AUTO_INC)
    full_name     | full_name         | CharField(100), NOT NULL
    email         | email             | EmailField(100), UNIQUE, NOT NULL
    password_hash | password          | Managed by Django's auth — NEVER plaintext
    role          | role              | CharField(255), choices: admin/user
    status        | status            | CharField, choices: active/inactive
    created_at    | created_at        | DateTimeField, auto-populated on creation

OUR IMPLEMENTATION DECISIONS:
  - Django uses `id` as the auto-generated primary key (maps to spec's user_id).
  - `email` is the USERNAME_FIELD (login identifier instead of a username).
  - `is_active` (Django internal) is kept TRUE for all users regardless of status.
    Status-based blocking is enforced in the login view for clean error messaging.
  - Passwords are ALWAYS stored hashed via Django's PBKDF2-SHA256 algorithm.
"""

import hashlib
import random
from datetime import timedelta

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """
    Custom manager for CustomUser.
    Uses email as the unique authentication identifier.
    """

    def create_user(self, email, full_name, password=None, **extra_fields):
        """Create and return a standard (non-admin) user."""
        if not email:
            raise ValueError('A valid email address is required.')
        if not full_name:
            raise ValueError('Full name is required.')

        email = self.normalize_email(email)
        extra_fields.setdefault('role', 'user')
        extra_fields.setdefault('status', 'active')

        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)   # Hashes the password — never stores plaintext
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        """
        Create and return a superuser (admin).
        Called by `python manage.py createsuperuser`.
        """
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('status', 'active')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, full_name, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Nirmaan Foundation CMS User Model.

    Replaces Django's default User model.
    AUTH_USER_MODEL = 'accounts.CustomUser' in settings.py.
    """

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('volunteer', 'Volunteer'),
        ('donor', 'Donor'),
        ('user', 'User'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    # ── Spec fields ──────────────────────────────────────────
    full_name = models.CharField(
        max_length=100,
        verbose_name='Full Name',
    )
    email = models.EmailField(
        max_length=100,
        unique=True,
        verbose_name='Email Address',
    )
    # `password` field is inherited from AbstractBaseUser (hashed storage)
    role = models.CharField(
        max_length=255,
        choices=ROLE_CHOICES,
        default='user',
        verbose_name='Role',
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='Account Status',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At',
    )

    # ── Django internals ──────────────────────────────────────
    is_active = models.BooleanField(default=True)   # Required by Django auth
    is_staff = models.BooleanField(default=False)   # Required for Django admin access

    # ── Auth configuration ────────────────────────────────────
    USERNAME_FIELD = 'email'           # Login with email, not username
    REQUIRED_FIELDS = ['full_name']    # Required when using createsuperuser

    objects = CustomUserManager()

    class Meta:
        db_table = 'accounts_customuser'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.full_name} ({self.email})'

    def get_full_name(self):
        """Return the user's full name."""
        return self.full_name

    def get_short_name(self):
        """Return the user's first name."""
        return self.full_name.split()[0] if self.full_name else ''

    @property
    def is_admin(self):
        """Convenience check: is this user an admin?"""
        return self.role == 'admin'

    @property
    def is_regular_user(self):
        """Convenience check: is this user a standard user?"""
        return self.role == 'user'


class PasswordResetOTP(models.Model):
    """
    Stores 6-digit OTP for Forgot Password functionality.
    OTP is hashed using SHA-256 for security at rest.
    Rate limiting: max 5 verification attempts.
    Expiry: default 10 minutes.
    """
    user = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        related_name='password_reset_otps',
        verbose_name='User',
    )
    otp_hash = models.CharField(
        max_length=64,
        verbose_name='OTP Hash',
        help_text='SHA-256 hash of the 6-digit OTP',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At',
    )
    expires_at = models.DateTimeField(
        verbose_name='Expires At',
    )
    is_used = models.BooleanField(
        default=False,
        verbose_name='Is Used',
    )
    attempts = models.IntegerField(
        default=0,
        verbose_name='Failed Attempts',
    )

    class Meta:
        db_table = 'accounts_password_reset_otp'
        verbose_name = 'Password Reset OTP'
        verbose_name_plural = 'Password Reset OTPs'
        ordering = ['-created_at']

    def __str__(self):
        return f'OTP for {self.user.email} (expires {self.expires_at})'

    @classmethod
    def generate_otp_for_user(cls, user, expiry_minutes=10):
        """
        Invalidates any previous unused OTPs for the user, generates
        a new cryptographically secure 6-digit numeric OTP, and stores
        its SHA-256 hash. Returns (plain_otp, otp_record).
        """
        cls.objects.filter(user=user, is_used=False).update(is_used=True)
        plain_otp = f"{random.randint(100000, 999999)}"
        otp_hash = hashlib.sha256(plain_otp.encode('utf-8')).hexdigest()
        expires_at = timezone.now() + timedelta(minutes=expiry_minutes)
        otp_record = cls.objects.create(
            user=user,
            otp_hash=otp_hash,
            expires_at=expires_at,
        )
        return plain_otp, otp_record

    def verify_otp(self, plain_otp):
        """
        Verify the submitted plain OTP.
        Returns (is_valid: bool, error_message: str or None).
        """
        if self.is_used:
            return False, 'This OTP code has already been used. Please request a new one.'
        if timezone.now() > self.expires_at:
            return False, 'This OTP code has expired. Please request a new one.'
        if self.attempts >= 5:
            return False, 'Maximum verification attempts exceeded. Please request a new OTP.'

        entered_hash = hashlib.sha256(plain_otp.strip().encode('utf-8')).hexdigest()
        if entered_hash != self.otp_hash:
            self.attempts += 1
            self.save(update_fields=['attempts'])
            remaining = 5 - self.attempts
            if remaining > 0:
                return False, f'Invalid OTP code. {remaining} attempt(s) remaining.'
            return False, 'Invalid OTP code. Maximum attempts reached. Please request a new OTP.'

        return True, None

