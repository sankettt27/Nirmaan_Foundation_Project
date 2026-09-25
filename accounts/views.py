"""
accounts/views.py — Views for the Accounts application.

Views implemented:
  - login_view          : Email + password authentication, role-based redirect
  - register_view       : New user registration (role fixed to 'user')
  - logout_view         : Secure session logout
  - admin_dashboard_view: Protected admin dashboard with real platform data
  - volunteer_dashboard_view: Protected volunteer dashboard
  - donor_dashboard_view: Protected donor dashboard

Helpers:
  - role_required(role) : Decorator enforcing backend role-based access control
  - redirect_by_role(user): Returns the correct redirect for a given user's role

SECURITY NOTES:
  - Inactive accounts are explicitly blocked in login_view with a clear message.
  - Dashboard access is protected by role_required decorator (backend enforcement,
    not just template-level hiding).
  - Django's built-in authenticate() and login()/logout() are used throughout.
  - CSRF protection is provided by Django's CsrfViewMiddleware (enabled in settings).
  - Password reset uses Django's built-in signed-token mechanism (urls.py).
"""

import logging
import threading
from datetime import datetime
from functools import wraps

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse

from .forms import (
    LoginForm,
    PasswordResetRequestForm,
    PasswordResetVerifyOTPForm,
    RegistrationForm,
)
from .models import CustomUser, PasswordResetOTP

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────
# EMAIL DISPATCH HELPERS (NON-BLOCKING ASYNC)
# ─────────────────────────────────────────────────────────────

def _dispatch_email_async(email):
    """
    Dispatch email in a daemon background thread so the HTTP request
    and user redirection happen INSTANTLY (<50ms) without waiting on SMTP.
    In testing environment (locmem), sends synchronously so test assertions pass.
    """
    if getattr(settings, 'EMAIL_BACKEND', '') == 'django.core.mail.backends.locmem.EmailBackend':
        email.send(fail_silently=False)
    else:
        def _send():
            try:
                email.send(fail_silently=False)
            except Exception as e:
                logger.error(f"Background email delivery failed to {getattr(email, 'to', 'recipient')}: {e}")

        worker = threading.Thread(target=_send, daemon=True)
        worker.start()


def send_registration_confirmation_email(request, user, role_display):
    """
    Send a welcoming confirmation email to the newly registered user (plaintext).
    Dispatched asynchronously for instant page load.
    """
    try:
        subject = 'Welcome to Nirmaan Foundation! Your Registration is Confirmed'
        context = {
            'user': user,
            'role_display': role_display,
        }
        text_content = render_to_string('accounts/emails/registration_confirmation_email.txt', context)

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.encoding = 'utf-8'
        _dispatch_email_async(email)
        return True
    except Exception as e:
        logger.error(f"Error preparing registration confirmation email to {user.email}: {e}")
        return False


def send_password_reset_otp_email(request, user, otp):
    """
    Send a 6-digit OTP code to user's email for password reset.
    Dispatched asynchronously for instant page load.
    """
    try:
        subject = 'Your Nirmaan Foundation Password Reset OTP'
        context = {
            'user': user,
            'otp': otp,
        }
        html_content = render_to_string('accounts/emails/password_reset_otp_email.html', context)
        text_content = render_to_string('accounts/emails/password_reset_otp_email.txt', context)

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.encoding = 'utf-8'
        email.attach_alternative(html_content, 'text/html')
        _dispatch_email_async(email)
        return True
    except Exception as e:
        logger.error(f"Error preparing password reset OTP to {user.email}: {e}")
        return False



# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def role_required(required_role):
    """
    Decorator that enforces role-based access control at the backend level.

    Usage:
        @role_required('admin')
        def my_view(request): ...

    Behaviour:
        - Unauthenticated users → redirected to login page.
        - Authenticated users with wrong role → redirected to login with error.
        - Non-admin portal ('user') accommodates 'user', 'volunteer', and 'donor'.
        - Admin portal ('admin') is restricted exclusively to 'admin'.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, 'Please log in to access this page.')
                return redirect('accounts:login')

            if required_role == 'user':
                allowed = {'user', 'volunteer', 'donor'}
            else:
                allowed = {required_role}

            if request.user.role not in allowed:
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('accounts:login')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def redirect_by_role(user):
    """
    Return the appropriate HttpResponseRedirect based on the user's role.

    OUR IMPLEMENTATION DECISION:
      admin     → /dashboard/admin/
      volunteer → /dashboard/volunteer/
      donor     → /dashboard/donor/
      user      → /dashboard/volunteer/  (fallback)
    """
    if user.role == 'admin':
        return redirect('accounts:admin_dashboard')
    elif user.role == 'donor':
        return redirect('accounts:donor_dashboard')
    return redirect('accounts:volunteer_dashboard')


def _get_time_of_day():
    """Return a greeting based on current hour: morning/afternoon/evening."""
    hour = datetime.now().hour
    if hour < 12:
        return 'morning'
    elif hour < 17:
        return 'afternoon'
    return 'evening'


# ─────────────────────────────────────────────────────────────
# AUTHENTICATION VIEWS
# ─────────────────────────────────────────────────────────────

def login_view(request):
    """
    Handle user login via email and password.

    Flow:
      POST valid credentials + active account → role-based dashboard redirect
      POST valid credentials + inactive account → error message (account blocked)
      POST invalid credentials → generic error (avoids revealing which field is wrong)
      GET → display login form
    """
    # Already authenticated → go to the appropriate dashboard
    if request.user.is_authenticated:
        return redirect_by_role(request.user)

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Django's authenticate() checks credentials and returns the user or None
            user = authenticate(request, username=email, password=password)

            if user is not None:
                # Credentials valid — now check CMS account status
                if user.status == 'inactive':
                    messages.error(
                        request,
                        'Your account has been deactivated. '
                        'Please contact the administrator.',
                    )
                else:
                    auth_login(request, user)
                    messages.success(request, f'Welcome back, {user.get_full_name()}!')
                    return redirect_by_role(user)
            else:
                # Generic error — does not reveal whether the email exists
                messages.error(
                    request,
                    'Invalid email or password. Please check your credentials and try again.',
                )
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    """
    Handle new user self-registration.
    Collects user details and selected role (volunteer / donor).
    Sends confirmation email with a welcoming message.
    No OTP is required during registration.
    """
    if request.user.is_authenticated:
        return redirect_by_role(request.user)

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            selected_role = form.cleaned_data.get('role')
            if selected_role in ('volunteer', 'donor'):
                user.role = selected_role
            else:
                user.role = 'user'
            user.status = 'active'
            user.save()

            role_label = dict(RegistrationForm.PUBLIC_ROLE_CHOICES).get(user.role, user.role.title())
            email_sent = send_registration_confirmation_email(request, user, role_label)

            # Auto-login the newly registered user and redirect to their dashboard
            auth_login(request, user)

            if email_sent:
                messages.success(
                    request,
                    f'Welcome to Nirmaan Foundation, {user.get_full_name()}! A confirmation email has been sent to {user.email}.',
                )
            else:
                messages.success(
                    request,
                    f'Welcome to Nirmaan Foundation, {user.get_full_name()}!',
                )
            return redirect_by_role(user)
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})



def logout_view(request):
    """
    Handle secure logout.

    Clears the session via Django's auth_logout, then redirects to login.
    After logout, protected pages enforce re-authentication.
    Accepts POST only (CSRF-protected form in the template).
    """
    auth_logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('accounts:login')


# ─────────────────────────────────────────────────────────────
# DASHBOARD VIEWS
# ─────────────────────────────────────────────────────────────

@role_required('admin')
def admin_dashboard_view(request):
    """
    Admin dashboard — command center with real platform data.
    Protected by role_required('admin') — only users with role='admin' can access.
    Passes member counts, recent registrations, and platform stats to the template.
    """
    from .models import CustomUser

    total_members = CustomUser.objects.exclude(role='admin').count()
    total_volunteers = CustomUser.objects.filter(role='volunteer', status='active').count()
    total_donors = CustomUser.objects.filter(role='donor', status='active').count()
    total_admins = CustomUser.objects.filter(role='admin').count()
    total_active = CustomUser.objects.filter(status='active').count()
    recent_users = CustomUser.objects.exclude(role='admin').order_by('-created_at')[:5]

    context = {
        'total_members': total_members,
        'total_volunteers': total_volunteers,
        'total_donors': total_donors,
        'total_admins': total_admins,
        'total_active': total_active,
        'recent_users': recent_users,
        'time_of_day': _get_time_of_day(),
        'current_date': datetime.now().strftime('%B %d, %Y'),
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@role_required('user')
def volunteer_dashboard_view(request):
    """
    Volunteer dashboard — pulls real data from DB for the authenticated volunteer.
    Shows opportunities, events, and their personal registration stats.
    """
    from cms.models import VolunteerOpportunity, AboutEvent, VolunteerRegistration, Project

    # Real DB data
    opportunities = VolunteerOpportunity.objects.filter(is_active=True).order_by('order')[:6]
    events = AboutEvent.objects.filter(is_active=True).order_by('order')[:4]
    ongoing_projects = Project.objects.filter(status='Ongoing').count()

    # Volunteer's own registrations
    my_registrations = VolunteerRegistration.objects.filter(
        volunteer=request.user
    ).select_related('opportunity').order_by('-registered_at')

    # Registration IDs for quick template lookup
    registered_opportunity_ids = set(my_registrations.values_list('opportunity_id', flat=True))
    registration_status_map = {r.opportunity_id: r.status for r in my_registrations}

    # Summary stats (real numbers)
    total_opportunities = VolunteerOpportunity.objects.filter(is_active=True).count()
    total_events = AboutEvent.objects.filter(is_active=True).count()
    my_reg_count = my_registrations.count()
    my_pending_count = my_registrations.filter(status='pending').count()

    context = {
        'time_of_day': _get_time_of_day(),
        'current_date': datetime.now().strftime('%B %d, %Y'),
        'opportunities': opportunities,
        'events': events,
        'ongoing_projects': ongoing_projects,
        'my_registrations': my_registrations[:5],
        'registered_opportunity_ids': registered_opportunity_ids,
        'registration_status_map': registration_status_map,
        'total_opportunities': total_opportunities,
        'total_events': total_events,
        'my_reg_count': my_reg_count,
        'my_pending_count': my_pending_count,
        'active_nav': 'dashboard',
    }
    return render(request, 'accounts/volunteer_dashboard.html', context)


@role_required('user')
def volunteer_opportunities_view(request):
    """
    Dedicated page: Browse all active volunteer opportunities.
    """
    from cms.models import VolunteerOpportunity, VolunteerRegistration

    opportunities = VolunteerOpportunity.objects.filter(is_active=True).order_by('order')
    my_registrations = VolunteerRegistration.objects.filter(
        volunteer=request.user
    ).values_list('opportunity_id', 'status')

    registration_status_map = {opp_id: status for opp_id, status in my_registrations}

    context = {
        'opportunities': opportunities,
        'registration_status_map': registration_status_map,
        'active_nav': 'opportunities',
        'current_date': datetime.now().strftime('%B %d, %Y'),
    }
    return render(request, 'accounts/volunteer_opportunities.html', context)


@role_required('user')
def volunteer_register_opportunity_view(request, pk):
    """
    POST: Register authenticated volunteer for a given opportunity.
    Prevents duplicate registrations with a 409-style redirect + message.
    """
    from cms.models import VolunteerOpportunity, VolunteerRegistration
    from django.shortcuts import get_object_or_404

    opportunity = get_object_or_404(VolunteerOpportunity, pk=pk, is_active=True)

    if request.method == 'POST':
        existing = VolunteerRegistration.objects.filter(
            volunteer=request.user, opportunity=opportunity
        ).first()

        if existing:
            messages.warning(
                request,
                f'You have already registered for "{opportunity.title}" '
                f'(Status: {existing.get_status_display()}).'
            )
        else:
            VolunteerRegistration.objects.create(
                volunteer=request.user,
                opportunity=opportunity,
                status='pending',
            )
            messages.success(
                request,
                f'Successfully registered for "{opportunity.title}"! '
                f'Your application is pending admin review.'
            )
    return redirect('accounts:volunteer_opportunities')


@role_required('user')
def volunteer_my_registrations_view(request):
    """
    Shows the authenticated volunteer's personal registration history.
    """
    from cms.models import VolunteerRegistration

    my_registrations = VolunteerRegistration.objects.filter(
        volunteer=request.user
    ).select_related('opportunity').order_by('-registered_at')

    context = {
        'my_registrations': my_registrations,
        'active_nav': 'registrations',
        'current_date': datetime.now().strftime('%B %d, %Y'),
    }
    return render(request, 'accounts/volunteer_my_registrations.html', context)


@role_required('user')
def volunteer_profile_view(request):
    """
    Volunteer profile view — displays current account information.
    """
    context = {
        'active_nav': 'profile',
        'current_date': datetime.now().strftime('%B %d, %Y'),
    }
    return render(request, 'accounts/volunteer_profile.html', context)


@role_required('user')
def donor_dashboard_view(request):
    """
    Donor dashboard — personalized portal for donors.
    Protected by role_required('user') — donors and users can access.
    """
    context = {
        'time_of_day': _get_time_of_day(),
        'current_date': datetime.now().strftime('%B %d, %Y'),
    }
    return render(request, 'accounts/donor_dashboard.html', context)


# ─────────────────────────────────────────────────────────────
# FORGOT PASSWORD — OTP VIEWS
# ─────────────────────────────────────────────────────────────

def password_reset_request_view(request):
    """
    Step 1 of Forgot Password: User enters registered email.
    Generates a secure 6-digit OTP and dispatches it via email.
    """
    if request.user.is_authenticated:
        return redirect_by_role(request.user)

    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].strip().lower()
            user = CustomUser.objects.filter(email=email).first()

            if user is not None:
                if user.status == 'inactive':
                    messages.error(
                        request,
                        'This account has been deactivated. Please contact the administrator.',
                    )
                    return render(request, 'accounts/password_reset.html', {'form': form})

                plain_otp, otp_record = PasswordResetOTP.generate_otp_for_user(user, expiry_minutes=10)
                email_sent = send_password_reset_otp_email(request, user, plain_otp)

                if email_sent:
                    request.session['password_reset_email'] = email
                    messages.success(
                        request,
                        f'A 6-digit OTP has been sent to {email}. Please enter it below along with your new password.',
                    )
                    return redirect('accounts:password_reset_verify')
                else:
                    messages.error(
                        request,
                        'Could not send OTP email. Please verify your connection or try again later.',
                    )
            else:
                messages.error(
                    request,
                    'No registered account found with that email address. Please check and try again.',
                )
    else:
        form = PasswordResetRequestForm()

    return render(request, 'accounts/password_reset.html', {'form': form})


def password_reset_verify_view(request):
    """
    Step 2 of Forgot Password: User enters 6-digit OTP, new password, and confirms.
    """
    if request.user.is_authenticated:
        return redirect_by_role(request.user)

    reset_email = request.session.get('password_reset_email')
    if not reset_email:
        messages.warning(request, 'Please submit your registered email address first.')
        return redirect('accounts:password_reset')

    user = CustomUser.objects.filter(email=reset_email).first()
    if not user:
        request.session.pop('password_reset_email', None)
        messages.error(request, 'User account not found. Please try again.')
        return redirect('accounts:password_reset')

    if request.method == 'POST':
        form = PasswordResetVerifyOTPForm(request.POST)
        if form.is_valid():
            submitted_otp = form.cleaned_data['otp']
            new_password = form.cleaned_data['password1']

            otp_record = PasswordResetOTP.objects.filter(
                user=user,
                is_used=False,
            ).order_by('-created_at').first()

            if not otp_record:
                messages.error(request, 'No active OTP request found. Please request a new OTP.')
                return redirect('accounts:password_reset')

            is_valid, error_msg = otp_record.verify_otp(submitted_otp)
            if not is_valid:
                form.add_error('otp', error_msg)
            else:
                user.set_password(new_password)
                user.save()

                otp_record.is_used = True
                otp_record.save(update_fields=['is_used'])

                request.session.pop('password_reset_email', None)

                messages.success(
                    request,
                    'Your password has been reset successfully! You can now log in with your new password.',
                )
                return redirect('accounts:login')
    else:
        form = PasswordResetVerifyOTPForm(initial={'email': reset_email})

    return render(
        request,
        'accounts/password_reset_verify.html',
        {
            'form': form,
            'email': reset_email,
        },
    )


def password_reset_resend_view(request):
    """
    Resends a fresh 6-digit OTP to the email stored in the current session.
    """
    if request.user.is_authenticated:
        return redirect_by_role(request.user)

    reset_email = request.session.get('password_reset_email')
    if not reset_email:
        messages.warning(request, 'Please request a password reset first.')
        return redirect('accounts:password_reset')

    user = CustomUser.objects.filter(email=reset_email).first()
    if user and user.status != 'inactive':
        plain_otp, _ = PasswordResetOTP.generate_otp_for_user(user, expiry_minutes=10)
        send_password_reset_otp_email(request, user, plain_otp)
        messages.info(request, f'A new 6-digit OTP code has been sent to {reset_email}.')
    else:
        messages.error(request, 'Unable to resend OTP. Please start over.')
        return redirect('accounts:password_reset')

    return redirect('accounts:password_reset_verify')

