"""
accounts/forms.py — Forms for the Accounts application.

Forms implemented:
  - LoginForm          : Email + password authentication
  - RegistrationForm   : New user registration (role fixed to 'user' — security decision)
"""

from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import CustomUser


# ─────────────────────────────────────────────────────────────
# LOGIN FORM
# ─────────────────────────────────────────────────────────────

class LoginForm(forms.Form):
    """
    Authentication form: email address + password.
    Does not extend AuthenticationForm because we use email, not username.
    """

    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'Enter your email address',
            'id': 'id_email',
            'autofocus': True,
            'autocomplete': 'email',
        }),
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'Enter your password',
            'id': 'id_password',
            'autocomplete': 'current-password',
        }),
    )


# ─────────────────────────────────────────────────────────────
# REGISTRATION FORM
# ─────────────────────────────────────────────────────────────

class RegistrationForm(forms.ModelForm):
    """
    New user registration form.

    SECURITY DECISION:
    Only public roles ('volunteer', 'donor') can be selected during self-registration.
    The 'admin' role is NEVER offered in the public registration form.
    Admin accounts can only be created via `python manage.py createsuperuser` or Django Admin.
    """

    PUBLIC_ROLE_CHOICES = [
        ('', 'Select your role'),
        ('volunteer', 'Volunteer'),
        ('donor', 'Donor'),
    ]

    role = forms.ChoiceField(
        choices=PUBLIC_ROLE_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control auth-input',
            'id': 'id_role',
        }),
        label='Role',
    )

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'Create a strong password (min. 8 characters)',
            'id': 'id_password1',
            'autocomplete': 'new-password',
        }),
    )

    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'Repeat your password',
            'id': 'id_password2',
            'autocomplete': 'new-password',
        }),
    )

    class Meta:
        model = CustomUser
        fields = ['full_name', 'role', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control auth-input',
                'placeholder': 'Enter your full name',
                'id': 'id_full_name',
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control auth-input',
                'placeholder': 'Enter your email address',
                'id': 'id_reg_email',
                'autocomplete': 'email',
            }),
        }

    def clean_role(self):
        """Sanitize role selection to only permit public roles (volunteer, donor)."""
        role = self.cleaned_data.get('role')
        if not role:
            return 'user'
        if role not in ('volunteer', 'donor'):
            return 'user'
        return role

    def clean_password1(self):
        """Run Django's built-in password validators against the chosen password."""
        password1 = self.cleaned_data.get('password1')
        if password1:
            try:
                validate_password(password1)
            except ValidationError as e:
                raise forms.ValidationError(e.messages)
        return password1

    def clean_password2(self):
        """Ensure both password fields match."""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match. Please try again.')
        return password2

    def save(self, commit=True):
        """
        Save the user with a hashed password and the sanitized role.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])  # Hashes the password
        role = self.cleaned_data.get('role') or 'user'
        if role not in ('volunteer', 'donor'):
            role = 'user'
        user.role = role
        user.status = 'active'
        if commit:
            user.save()
        return user


# ─────────────────────────────────────────────────────────────
# FORGOT PASSWORD — OTP FORMS
# ─────────────────────────────────────────────────────────────

class PasswordResetRequestForm(forms.Form):
    """
    Form to request a 6-digit OTP sent to the user's email address.
    """
    email = forms.EmailField(
        label='Registered Email Address',
        widget=forms.EmailInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'Enter your registered email address',
            'id': 'id_reset_email',
            'autocomplete': 'email',
            'autofocus': True,
        }),
    )


class PasswordResetVerifyOTPForm(forms.Form):
    """
    Form to verify the 6-digit OTP and set a new password.
    """
    email = forms.EmailField(
        widget=forms.HiddenInput(),
    )

    otp = forms.CharField(
        label='6-Digit OTP Code',
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control auth-input text-center fw-bold',
            'placeholder': '• • • • • •',
            'id': 'id_otp',
            'autocomplete': 'one-time-code',
            'inputmode': 'numeric',
            'pattern': '[0-9]{6}',
            'maxlength': '6',
            'style': 'letter-spacing: 8px; font-size: 1.25rem;',
            'autofocus': True,
        }),
    )

    password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'Enter new password (min. 8 characters)',
            'id': 'id_new_password1',
            'autocomplete': 'new-password',
        }),
    )

    password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'Confirm your new password',
            'id': 'id_new_password2',
            'autocomplete': 'new-password',
        }),
    )

    def clean_otp(self):
        otp = self.cleaned_data.get('otp', '').strip()
        if not otp.isdigit() or len(otp) != 6:
            raise forms.ValidationError('Please enter a valid 6-digit numeric OTP code.')
        return otp

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            try:
                validate_password(password1)
            except ValidationError as e:
                raise forms.ValidationError(e.messages)
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match. Please try again.')
        return password2

