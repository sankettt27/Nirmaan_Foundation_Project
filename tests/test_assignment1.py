"""
tests/test_assignment1.py — Assignment 1: User Login and Registration System

Tests cover:
  1. Registration — valid, duplicate email, password mismatch, required fields
  2. Login — valid credentials, invalid credentials, inactive account, role redirect
  3. Authorization — dashboard access control, role enforcement
  4. Logout — session cleared, protected page inaccessible after logout
  5. Security — passwords hashed, CSRF tokens present, role cannot be escalated

Run with:
    python manage.py test tests.test_assignment1
"""

from django.contrib.auth import SESSION_KEY
from django.core import mail
from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import CustomUser, PasswordResetOTP


# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def make_user(email='user@example.com', full_name='Test User',
              password='TestP@ss99', role='user', status='active'):
    """Create a CustomUser for use in tests."""
    return CustomUser.objects.create_user(
        email=email,
        full_name=full_name,
        password=password,
        role=role,
        status=status,
    )


def make_admin(email='admin@example.com', full_name='Admin User',
               password='AdminP@ss99'):
    """Create an admin CustomUser for use in tests."""
    return CustomUser.objects.create_user(
        email=email,
        full_name=full_name,
        password=password,
        role='admin',
        status='active',
    )


# ─────────────────────────────────────────────────────────────
# 1. REGISTRATION TESTS
# ─────────────────────────────────────────────────────────────

class RegistrationTests(TestCase):
    """Tests for the user registration view and form."""

    def setUp(self):
        self.client = Client()
        self.url = reverse('accounts:register')
        self.valid_data = {
            'full_name': 'Jane Doe',
            'email': 'jane@example.com',
            'password1': 'StrongP@ss77',
            'password2': 'StrongP@ss77',
        }

    def test_register_page_loads(self):
        """GET /register/ returns 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_valid_registration_creates_user(self):
        """Valid POST creates a user, logs them in, and redirects to dashboard."""
        response = self.client.post(self.url, self.valid_data)
        self.assertRedirects(response, reverse('accounts:volunteer_dashboard'))
        self.assertTrue(CustomUser.objects.filter(email='jane@example.com').exists())

    def test_registered_user_has_role_user(self):
        """
        Registration ALWAYS creates role='user'.
        Security decision: admin role cannot be obtained via the public form.
        """
        self.client.post(self.url, self.valid_data)
        user = CustomUser.objects.get(email='jane@example.com')
        self.assertEqual(user.role, 'user')

    def test_registered_user_has_active_status(self):
        """Newly registered users are active by default."""
        self.client.post(self.url, self.valid_data)
        user = CustomUser.objects.get(email='jane@example.com')
        self.assertEqual(user.status, 'active')

    def test_password_stored_hashed(self):
        """Password must be stored hashed — never as plaintext."""
        self.client.post(self.url, self.valid_data)
        user = CustomUser.objects.get(email='jane@example.com')
        # The stored password must not equal the plaintext password
        self.assertNotEqual(user.password, 'StrongP@ss77')
        # Django's check_password verifies the hash correctly
        self.assertTrue(user.check_password('StrongP@ss77'))

    def test_registration_sends_confirmation_email(self):
        """Newly registered user receives a confirmation email."""
        mail.outbox.clear()
        self.client.post(self.url, self.valid_data)
        self.assertEqual(len(mail.outbox), 1)
        sent_email = mail.outbox[0]
        self.assertIn('jane@example.com', sent_email.to)
        self.assertIn('Registration is Confirmed', sent_email.subject)

    def test_duplicate_email_rejected(self):
        """Registration with an existing email must fail."""
        make_user(email='jane@example.com')
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 200)
        # Only one user with this email should exist
        self.assertEqual(CustomUser.objects.filter(email='jane@example.com').count(), 1)

    def test_mismatched_passwords_rejected(self):
        """Passwords that don't match must be rejected."""
        data = {**self.valid_data, 'password2': 'DifferentP@ss99'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CustomUser.objects.filter(email='jane@example.com').exists())

    def test_missing_full_name_rejected(self):
        """Missing full_name must be rejected."""
        data = {**self.valid_data, 'full_name': ''}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CustomUser.objects.filter(email='jane@example.com').exists())

    def test_missing_email_rejected(self):
        """Missing email must be rejected."""
        data = {**self.valid_data, 'email': ''}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)

    def test_weak_password_rejected(self):
        """Django's password validators must reject a too-short password."""
        data = {**self.valid_data, 'password1': 'abc', 'password2': 'abc'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CustomUser.objects.filter(email='jane@example.com').exists())

    def test_authenticated_user_redirected_away_from_register(self):
        """A logged-in user visiting /register/ should be redirected to dashboard."""
        user = make_user()
        self.client.force_login(user)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('accounts:volunteer_dashboard'))


# ─────────────────────────────────────────────────────────────
# 2. LOGIN TESTS
# ─────────────────────────────────────────────────────────────

class LoginTests(TestCase):
    """Tests for the login view."""

    def setUp(self):
        self.client = Client()
        self.url = reverse('accounts:login')
        self.admin = make_admin()
        self.regular_user = make_user()
        self.inactive_user = make_user(
            email='inactive@example.com',
            full_name='Inactive User',
            status='inactive',
        )

    def test_login_page_loads(self):
        """GET /login/ returns 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_admin_login_redirects_to_admin_dashboard(self):
        """Admin credentials → redirect to /dashboard/admin/."""
        response = self.client.post(self.url, {
            'email': 'admin@example.com',
            'password': 'AdminP@ss99',
        })
        self.assertRedirects(response, reverse('accounts:admin_dashboard'))

    def test_user_login_redirects_to_user_dashboard(self):
        """User credentials → redirect to /dashboard/user/."""
        response = self.client.post(self.url, {
            'email': 'user@example.com',
            'password': 'TestP@ss99',
        })
        self.assertRedirects(response, reverse('accounts:volunteer_dashboard'))

    def test_invalid_password_rejected(self):
        """Wrong password → 200 (form re-rendered), no session."""
        response = self.client.post(self.url, {
            'email': 'user@example.com',
            'password': 'WrongPassword!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_nonexistent_email_rejected(self):
        """Non-existent email → 200 (generic error, no session)."""
        response = self.client.post(self.url, {
            'email': 'nobody@example.com',
            'password': 'SomePassword123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_inactive_account_blocked(self):
        """Inactive account must not be authenticated, even with valid credentials."""
        response = self.client.post(self.url, {
            'email': 'inactive@example.com',
            'password': 'TestP@ss99',
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_authenticated_user_redirected_from_login(self):
        """A logged-in user visiting /login/ should be redirected to their dashboard."""
        self.client.force_login(self.regular_user)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('accounts:volunteer_dashboard'))


# ─────────────────────────────────────────────────────────────
# 3. AUTHORIZATION TESTS
# ─────────────────────────────────────────────────────────────

class AuthorizationTests(TestCase):
    """Tests for backend authorization (role_required decorator)."""

    def setUp(self):
        self.client = Client()
        self.admin = make_admin()
        self.regular_user = make_user()
        self.admin_url = reverse('accounts:admin_dashboard')
        self.user_url = reverse('accounts:user_dashboard')

    def test_unauthenticated_cannot_access_admin_dashboard(self):
        """Anonymous user is redirected away from admin dashboard."""
        response = self.client.get(self.admin_url)
        self.assertRedirects(response, reverse('accounts:login'))

    def test_unauthenticated_cannot_access_user_dashboard(self):
        """Anonymous user is redirected away from user dashboard."""
        response = self.client.get(self.user_url)
        self.assertRedirects(response, reverse('accounts:login'))

    def test_admin_can_access_admin_dashboard(self):
        """Admin user can access the admin dashboard."""
        self.client.force_login(self.admin)
        response = self.client.get(self.admin_url)
        self.assertEqual(response.status_code, 200)

    def test_user_can_access_user_dashboard(self):
        """Standard user can access the user dashboard."""
        self.client.force_login(self.regular_user)
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, 200)

    def test_user_cannot_access_admin_dashboard(self):
        """Standard user must NOT access the admin dashboard."""
        self.client.force_login(self.regular_user)
        response = self.client.get(self.admin_url)
        # Must be redirected (not granted access)
        self.assertNotEqual(response.status_code, 200)

    def test_admin_cannot_access_user_dashboard(self):
        """Admin must NOT access the user dashboard (wrong role)."""
        self.client.force_login(self.admin)
        response = self.client.get(self.user_url)
        self.assertNotEqual(response.status_code, 200)


# ─────────────────────────────────────────────────────────────
# 4. LOGOUT TESTS
# ─────────────────────────────────────────────────────────────

class LogoutTests(TestCase):
    """Tests for logout view."""

    def setUp(self):
        self.client = Client()
        self.user = make_user()
        self.logout_url = reverse('accounts:logout')
        self.user_dashboard_url = reverse('accounts:user_dashboard')

    def test_logout_redirects_to_login(self):
        """POST /logout/ redirects to /login/."""
        self.client.force_login(self.user)
        response = self.client.post(self.logout_url)
        self.assertRedirects(response, reverse('accounts:login'))

    def test_dashboard_inaccessible_after_logout(self):
        """After logout, the dashboard must not be accessible."""
        self.client.force_login(self.user)
        # Confirm access before logout
        self.assertEqual(self.client.get(self.user_dashboard_url).status_code, 200)
        # Logout
        self.client.post(self.logout_url)
        # Now must be redirected
        response = self.client.get(self.user_dashboard_url)
        self.assertRedirects(response, reverse('accounts:login'))

    def test_session_cleared_after_logout(self):
        """Session authentication key must not exist after logout."""
        self.client.force_login(self.user)
        self.assertIn(SESSION_KEY, self.client.session)
        self.client.post(self.logout_url)
        self.assertNotIn(SESSION_KEY, self.client.session)


# ─────────────────────────────────────────────────────────────
# 5. SECURITY TESTS
# ─────────────────────────────────────────────────────────────

class SecurityTests(TestCase):
    """Tests for security properties of Assignment 1."""

    def setUp(self):
        self.client = Client()

    def test_login_form_contains_csrf_token(self):
        """Login page must include a CSRF token in the form."""
        response = self.client.get(reverse('accounts:login'))
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_register_form_contains_csrf_token(self):
        """Registration page must include a CSRF token in the form."""
        response = self.client.get(reverse('accounts:register'))
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_password_never_stored_as_plaintext(self):
        """Verifies the stored password value is a hash, not plaintext."""
        user = make_user(password='PlainTextPass1!')
        self.assertNotEqual(user.password, 'PlainTextPass1!')
        # Django hashed passwords start with the algorithm identifier
        self.assertIn('$', user.password)

    def test_cannot_escalate_to_admin_via_registration(self):
        """
        Attempting to POST a role value to registration must NOT create an admin.
        The view ignores any role submitted and always sets role='user'.
        """
        response = self.client.post(reverse('accounts:register'), {
            'full_name': 'Hacker',
            'email': 'hacker@example.com',
            'password1': 'StrongP@ss77',
            'password2': 'StrongP@ss77',
            'role': 'admin',   # Attempting privilege escalation
        })
        # If the user was created, check their role
        if CustomUser.objects.filter(email='hacker@example.com').exists():
            user = CustomUser.objects.get(email='hacker@example.com')
            self.assertEqual(user.role, 'user')  # Must still be 'user'


# ─────────────────────────────────────────────────────────────
# 6. USER MODEL TESTS
# ─────────────────────────────────────────────────────────────

class UserModelTests(TestCase):
    """Tests for CustomUser model properties and manager."""

    def test_create_user_requires_email(self):
        """Creating a user without email must raise ValueError."""
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(email='', full_name='No Email', password='pass')

    def test_create_user_requires_full_name(self):
        """Creating a user without full_name must raise ValueError."""
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(email='x@x.com', full_name='', password='pass')

    def test_create_superuser_sets_admin_role(self):
        """create_superuser must set role='admin'."""
        admin = CustomUser.objects.create_superuser(
            email='sup@example.com',
            full_name='Super User',
            password='AdminP@ss99',
        )
        self.assertEqual(admin.role, 'admin')
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_is_admin_property(self):
        """is_admin property returns True only for admin role."""
        admin = make_admin()
        user = make_user()
        self.assertTrue(admin.is_admin)
        self.assertFalse(user.is_admin)

    def test_str_representation(self):
        """__str__ returns name and email."""
        user = make_user(full_name='John Smith', email='john@example.com')
        self.assertIn('John Smith', str(user))
        self.assertIn('john@example.com', str(user))

    def test_get_full_name(self):
        """get_full_name() returns the full_name field."""
        user = make_user(full_name='Jane Doe')
        self.assertEqual(user.get_full_name(), 'Jane Doe')

    def test_get_short_name(self):
        """get_short_name() returns the first word of full_name."""
        user = make_user(full_name='Jane Doe')
        self.assertEqual(user.get_short_name(), 'Jane')


# ─────────────────────────────────────────────────────────────
# 6. PASSWORD RESET OTP TESTS
# ─────────────────────────────────────────────────────────────

class PasswordResetOTPTests(TestCase):
    """Tests for the 6-digit OTP password reset system."""

    def setUp(self):
        self.client = Client()
        self.user = make_user(
            email='resetuser@example.com',
            full_name='Reset Test User',
            password='OldP@ssword123',
        )
        self.reset_url = reverse('accounts:password_reset')
        self.verify_url = reverse('accounts:password_reset_verify')
        self.resend_url = reverse('accounts:password_reset_resend')

    def test_password_reset_request_sends_otp(self):
        """Requesting password reset dispatches a 6-digit OTP email."""
        mail.outbox.clear()
        response = self.client.post(self.reset_url, {'email': 'resetuser@example.com'})
        self.assertRedirects(response, self.verify_url)
        self.assertEqual(len(mail.outbox), 1)
        sent_email = mail.outbox[0]
        self.assertIn('resetuser@example.com', sent_email.to)
        self.assertIn('Password Reset OTP', sent_email.subject)
        # Check OTP record created
        otp_record = PasswordResetOTP.objects.filter(user=self.user, is_used=False).first()
        self.assertIsNotNone(otp_record)

    def test_password_reset_verify_resets_password(self):
        """Entering the valid OTP and new password updates password."""
        plain_otp, otp_record = PasswordResetOTP.generate_otp_for_user(self.user)
        # Set session
        session = self.client.session
        session['password_reset_email'] = self.user.email
        session.save()

        response = self.client.post(self.verify_url, {
            'email': self.user.email,
            'otp': plain_otp,
            'password1': 'BrandNewP@ss99',
            'password2': 'BrandNewP@ss99',
        })
        self.assertRedirects(response, reverse('accounts:login'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('BrandNewP@ss99'))
        otp_record.refresh_from_db()
        self.assertTrue(otp_record.is_used)

    def test_password_reset_invalid_otp_fails(self):
        """Submitting an invalid OTP code does not change password."""
        plain_otp, otp_record = PasswordResetOTP.generate_otp_for_user(self.user)
        session = self.client.session
        session['password_reset_email'] = self.user.email
        session.save()

        response = self.client.post(self.verify_url, {
            'email': self.user.email,
            'otp': '000000',
            'password1': 'BrandNewP@ss99',
            'password2': 'BrandNewP@ss99',
        })
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password('BrandNewP@ss99'))
        self.assertTrue(self.user.check_password('OldP@ssword123'))

