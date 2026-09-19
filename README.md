# Nirmaan Foundation — NGO Content Management System

A web-based NGO Content Management System built with Python/Django,
developed progressively through internship assignments.

---

## Current Assignment

**Assignment 1 — User Login and Registration System**

Implements a complete authentication system with secure login, user registration,
role-based access control (Admin / User), session management, and password reset.

---

## Technology Stack

| Layer      | Technology                              |
|------------|-----------------------------------------|
| Backend    | Python 3.14, Django 5.2                 |
| Database   | MySQL (via PyMySQL)                     |
| Frontend   | Django Templates, HTML, CSS, Bootstrap 5|
| Auth       | Django Authentication Framework         |
| Email      | Console (dev) / SMTP (production)       |
| Config     | django-environ (.env)                   |

---

## Project Structure

```
Nirmaan_Foundation/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── config/               <- Django project settings
│   ├── __init__.py       <- PyMySQL patch
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/             <- Assignment 1: Authentication app
│   ├── migrations/
│   ├── models.py         <- CustomUser model
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── templates/
│   ├── base_auth.html
│   ├── base.html
│   └── accounts/
│       ├── login.html
│       ├── register.html
│       ├── admin_dashboard.html
│       ├── user_dashboard.html
│       └── password_reset*.html
├── static/css/auth.css
├── docs/assignment-1-authentication.md
└── tests/test_assignment1.py
```

---

## Installation

### Prerequisites

- Python 3.12+
- MySQL Server (installed and running)
- pip

### 1. Clone the repository

```bash
git clone <repository-url>
cd Nirmaan_Foundation
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` with your values. Generate a secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Create the MySQL database

```sql
CREATE DATABASE nirmaan_foundation CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Run migrations

```bash
python manage.py makemigrations accounts
python manage.py migrate
```

### 6. Create the initial administrator

```bash
python manage.py createsuperuser
```

> Admin accounts can ONLY be created this way or via Django Admin.
> The public registration form always creates user-role accounts.

### 7. Run the development server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/login/

---

## Authentication Flow

```
Registration (/register/) -> role always 'user' -> /login/
Login (/login/) -> admin -> /dashboard/admin/
                -> user  -> /dashboard/user/
Forgot Password -> email sent (console in dev) -> reset link -> /login/
Logout (/logout/) -> session cleared -> /login/
```

---

## URL Reference

| URL | Description | Access |
|-----|-------------|--------|
| `/login/` | Sign In | Public |
| `/register/` | Create Account | Public |
| `/logout/` | Sign Out | Authenticated (POST) |
| `/dashboard/admin/` | Admin Dashboard | role=admin only |
| `/dashboard/user/` | User Dashboard | role=user only |
| `/password-reset/` | Request Reset | Public |
| `/admin/` | Django Admin | is_staff=True |

---

## Session Management

- Inactivity timeout: **30 minutes**
- Timer resets on every request
- After 30 min inactivity, user is redirected to `/login/`

---

## Email Configuration

**Development** (default — prints to terminal):

```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

**Production** (configure SMTP in .env):

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
```

---

## Running Tests

```bash
python manage.py test tests.test_assignment1
```

---

## Security Highlights

- Passwords stored with PBKDF2-SHA256 (never plaintext)
- CSRF protection on all POST forms
- Role-based access enforced at the backend (not just UI)
- Admin accounts cannot be created via public registration
- All secrets loaded from .env (never hardcoded)
- Password reset uses Django's signed-token mechanism

---

## Documentation

See [docs/assignment-1-authentication.md](docs/assignment-1-authentication.md)
