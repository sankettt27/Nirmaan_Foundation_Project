# Assignment 1 — User Login and Registration System

**Project:** Nirmaan Foundation — NGO Content Management System
**Assignment:** 1 of ongoing internship
**Status:** Implemented

---

## 1. Objective

Implement a complete User Login and Registration System for the Nirmaan Foundation CMS,
providing secure authentication, role-based access control, session management, and
password reset functionality.

---

## 2. Technologies Used

| Component | Technology |
|-----------|------------|
| Language | Python 3.14 |
| Framework | Django 5.2 |
| Database | MySQL (via PyMySQL — pure Python adapter) |
| Frontend | Django Templates, HTML, CSS, Bootstrap 5 |
| Auth | Django's built-in authentication framework |
| Email | Console backend (dev) / SMTP (production) |
| Config | django-environ (`.env` file) |

---

## 3. Features Implemented

### Required by Assignment

- [x] Secure login using email and password
- [x] Authentication of credentials via Django auth backend
- [x] Redirect to Dashboard on successful login
- [x] Role-based access (Admin / User)
- [x] User registration
- [x] Forgot Password / Password Reset via email
- [x] Secure logout
- [x] Session management with inactivity timeout

### Our Implementation Decisions

- Single login page at `/login/` for both Admin and User accounts
- Backend determines role from authenticated account (user does NOT select role at login)
- Admin accounts are created via `python manage.py createsuperuser` only
- Registration always assigns `role=user` — never `role=admin` (privilege escalation prevention)
- 30-minute inactivity timeout via `SESSION_COOKIE_AGE=1800`
- Console email backend for development (password reset emails print to terminal)

---

## 4. Authentication Flow

### Login

```
User visits /login/
    ↓
Email + Password submitted (CSRF-protected POST)
    ↓
Django authenticate() verifies credentials
    ↓
Credentials invalid? → Show generic error message
    ↓
Account status == 'inactive'? → Block login with message
    ↓
role == 'admin' → Redirect to /dashboard/admin/
role == 'user'  → Redirect to /dashboard/user/
```

### Registration

```
User visits /register/
    ↓
Full Name + Email + Password + Confirm Password
    ↓
Form validated (duplicate email check, password validators)
    ↓
User created with role='user', status='active'
    ↓
Redirect to /login/
```

### Logout

```
User clicks Logout (CSRF-protected POST)
    ↓
Django auth_logout() — session cleared
    ↓
Redirect to /login/
    ↓
Protected pages now require re-authentication
```

---

## 5. Role Handling

**OUR IMPLEMENTATION DECISION** (not explicitly prescribed by internship document):

| Role | Login Destination | Dashboard |
|------|-------------------|-----------|
| `admin` | `/dashboard/admin/` | Admin Dashboard |
| `user` | `/dashboard/user/` | User Dashboard |

Role is determined from the authenticated user account.
Users do NOT select their role at the login screen.

### Backend Authorization

A reusable `role_required(role)` decorator is implemented in `accounts/views.py`.
It enforces access control at the backend — not just by hiding UI elements.

```
@role_required('admin')
def admin_dashboard_view(request): ...

@role_required('user')
def user_dashboard_view(request): ...
```

---

## 6. Password Reset Flow

Uses Django's built-in signed-token password reset mechanism.

```
/password-reset/            → Enter registered email
    ↓
Email sent with signed reset link (console backend in dev)
    ↓
/password-reset/done/       → Confirmation page
    ↓
User clicks link in email
    ↓
/password-reset/confirm/<uid>/<token>/  → Set new password
    ↓
/password-reset/complete/   → Success message
    ↓
/login/                     → Login with new password
```

If the reset link is expired or already used, an error is shown with an option
to request a new link.

---

## 7. Session Management

| Setting | Value | Effect |
|---------|-------|--------|
| `SESSION_COOKIE_AGE` | 1800 (30 min) | Session expires after 30 min inactivity |
| `SESSION_SAVE_EVERY_REQUEST` | `True` | Timer resets on every request |
| `SESSION_EXPIRE_AT_BROWSER_CLOSE` | `False` | Session respects cookie age |

**OUR IMPLEMENTATION DECISION:** 30-minute inactivity timeout was chosen as
a reasonable balance between usability and security for an NGO CMS admin system.

---

## 8. Database Structure

### CustomUser Model

Maps to the Users table specified in the internship documentation:

| Spec Field | Django Field | Type | Constraints |
|------------|-------------|------|-------------|
| `user_id` | `id` | BigAutoField | PRIMARY KEY, AUTO_INCREMENT |
| `full_name` | `full_name` | CharField(100) | NOT NULL |
| `email` | `email` | EmailField(100) | UNIQUE, NOT NULL |
| `password_hash` | `password` | CharField(128) | NOT NULL, ALWAYS HASHED |
| `role` | `role` | CharField(255) | choices: admin/user |
| `status` | `status` | CharField(20) | choices: active/inactive, DEFAULT active |
| `created_at` | `created_at` | DateTimeField | auto_now_add=True |

**Note on `user_id`:** Django auto-creates an `id` field (BigAutoField, INT PK AUTO_INC).
This maps exactly to the spec's `user_id`. The Django convention `id` is used rather than
renaming it to `user_id` — this is **OUR IMPLEMENTATION DECISION**.

---

## 9. Security

### Password Security

- Django's PBKDF2-SHA256 algorithm used for all password hashing
- Passwords are NEVER stored in plaintext
- Passwords are NEVER logged
- Passwords are NEVER returned via templates or APIs
- Django's built-in `AUTH_PASSWORD_VALIDATORS` enforce minimum strength

### CSRF Protection

- Django's `CsrfViewMiddleware` is active
- All POST forms include `{% csrf_token %}`
- Login form, registration form, logout form, password reset forms are all CSRF-protected

### Session Security

- Django session framework handles session management
- Session cleared on logout (`auth_logout()`)
- 30-minute inactivity timeout configured

### Authorization

- Backend `role_required()` decorator enforces role access
- Unauthorized access results in redirect, not error exposure
- Unauthenticated users cannot access any dashboard URL

### Environment Variables

All sensitive configuration is loaded from `.env` via `django-environ`:
- `SECRET_KEY`
- `DB_PASSWORD`
- `EMAIL_HOST_PASSWORD`

`.env` is excluded from version control by `.gitignore`.
`.env.example` contains placeholder variable names only.

### Input Validation

- Django form validation for all inputs
- Email uniqueness checked at model level
- Password validators check minimum length, common passwords, numeric-only
- Django ORM used throughout — no raw SQL

### Error Messages

- Login failures show generic error (does not reveal whether email exists)
- Password reset shows generic success (does not reveal whether email is registered)

---

## 10. Testing

### How to Run

```bash
python manage.py test tests.test_assignment1
```

### Test Coverage

| Test Class | What It Tests |
|------------|--------------|
| `RegistrationTests` | Valid registration, duplicate email, password mismatch, weak password, role fixed to user, hashed password, missing fields |
| `LoginTests` | Valid login (admin), valid login (user), invalid password, non-existent email, inactive account, authenticated redirect |
| `AuthorizationTests` | Unauthenticated → redirected, admin can access admin dashboard, user can access user dashboard, cross-role access denied |
| `LogoutTests` | Logout redirects to login, dashboard inaccessible after logout, session cleared |
| `SecurityTests` | CSRF tokens present, password never plaintext, privilege escalation via registration blocked |
| `UserModelTests` | Manager validation, create_superuser sets admin role, is_admin property, __str__, get_full_name/short_name |

---

## 11. Files Created / Modified

| File | Action | Description |
|------|--------|-------------|
| `manage.py` | Created | Django management utility |
| `config/__init__.py` | Created | PyMySQL patch |
| `config/settings.py` | Created | Full Django settings |
| `config/urls.py` | Created | Root URL configuration |
| `config/wsgi.py` | Created | WSGI entry point |
| `config/asgi.py` | Created | ASGI entry point |
| `accounts/__init__.py` | Created | Package init |
| `accounts/models.py` | Created | CustomUser model |
| `accounts/admin.py` | Created | Django Admin registration |
| `accounts/apps.py` | Created | App configuration |
| `accounts/forms.py` | Created | LoginForm, RegistrationForm |
| `accounts/views.py` | Created | All auth views + role_required decorator |
| `accounts/urls.py` | Created | All auth URL patterns |
| `accounts/migrations/__init__.py` | Created | Migrations package |
| `templates/base_auth.html` | Created | Auth page base template |
| `templates/base.html` | Created | Dashboard base template |
| `templates/accounts/*.html` | Created | All auth/dashboard templates |
| `templates/accounts/emails/*` | Created | Password reset email templates |
| `static/css/auth.css` | Created | Auth and dashboard CSS |
| `requirements.txt` | Updated | Django, PyMySQL, django-environ |
| `.env.example` | Updated | All environment variable templates |
| `.env` | Created | Local dev config (gitignored) |
| `.gitignore` | Updated | Standard Django gitignore |
| `README.md` | Updated | Project documentation |
| `tests/test_assignment1.py` | Created | Comprehensive test suite |
| `docs/assignment-1-authentication.md` | Created | This document |
