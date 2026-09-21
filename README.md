# Nirmaan Foundation — NGO Management Platform

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Render-brightgreen?style=for-the-badge&logo=render)](https://nirmaan-foundation-project.onrender.com/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?style=for-the-badge&logo=github)](https://github.com/sankettt27/Nirmaan_Foundation_Project)
[![Django](https://img.shields.io/badge/Django-5.2-darkgreen?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)

A modern, web-based NGO Management and Content Platform for **Nirmaan Foundation**, built using Python and Django. Developed progressively with an emphasis on production security, responsive design, and intuitive role-based user experiences.

---

## 🚀 Live Demonstration

- **Live Application:** [https://nirmaan-foundation-project.onrender.com/](https://nirmaan-foundation-project.onrender.com/)
- **GitHub Repository:** [https://github.com/sankettt27/Nirmaan_Foundation_Project](https://github.com/sankettt27/Nirmaan_Foundation_Project)

### 🔑 Test Credentials (Live & Local)

| Role | Email | Password | Destination Dashboard |
|:---|:---|:---|:---|
| **System Administrator** | `admin@nirmaan.org` | `Admin@123` | `/dashboard/admin/` |
| **New Volunteer / User** | Register any new account at `/register/` | Your choice | `/dashboard/volunteer/` |

---

## 📌 Assignment 1 — User Authentication & Registration System

Implements an end-to-end authentication ecosystem:
- **Secure Email Authentication:** Case-insensitive email authentication with PBKDF2-SHA256 password hashing.
- **User Registration:** Dynamic validation, client/server sanitization, password complexity verification, and confirmation email dispatch.
- **Role-Based Experience:**
  - **Admin Dashboard (`/dashboard/admin/`):** Real-time platform metrics, user counts, registration analytics, system health, and administrative quick actions.
  - **Volunteer Dashboard (`/dashboard/volunteer/`):** Impact hours, upcoming community drives, engagement badges, and activity timeline.
  - **Donor Dashboard (`/dashboard/donor/`):** Contribution history, donation metrics, tax receipts, and impact stories.
- **Self-Service Password Recovery:** Secure 6-digit OTP email verification and signed reset tokens.
- **Session & Inactivity Management:** 30-minute rolling inactivity session timeout with CSRF protection on all state-altering requests.
- **Modern UI/UX:** Warm, accessible non-profit branding inspired by modern CRM platforms (Keela-style clean card architecture, responsive 50/50 split auth layout).

---

## 📌 Assignment 2 — Home Page Content Management System (CMS) & Sub-Pages

Implements a dynamic, non-technical Content Management System enabling full administrative control over public-facing media and narratives:
- **Core CMS Modules (`/dashboard/admin/home/`):**
  - **Hero Slider / Banners:** Upload, title, subtitle, CTA destination, order, active/draft toggle.
  - **Vision & Mission Statements:** Individual statement blocks with icon selector and display sequence.
  - **Impact Statistics:** Numeric counters and labels with soft-delete toggle.
  - **Initiatives & Flagship Programs:** Category tags, short cards, curriculum highlights, and beneficiaries reached.
- **6 Dedicated Public Sub-Pages (Bhumi.ngo Design Reference):**
  - **About Us (`/about/`):** Milestone timeline journey, executive leadership team, and events gallery.
  - **Programs (`/programs/`):** Full program directory, curriculum frameworks, and pedagogy highlights.
  - **Impact (`/impact/`):** Social metrics, student transformation case studies, and audited annual reports.
  - **Volunteer (`/volunteer/`):** 4-step volunteer roadmap, open role listings, and volunteer FAQs.
  - **Partner With Us (`/partner/`):** Corporate CSR turnkey models, 80G tax benefit notes, and partner logo wall.
  - **Contact Us (`/contact/`):** Working message inquiry form, national HQ & chapter office cards, and helpline touchpoints.
- **Image Size & Aspect Ratio Guidance in Brackets:**
  - Every form input explicitly guides admins with optimal image dimensions directly in the field label (e.g. `Banner Image (Recommended: 1920 × 800 px · 16:9 ratio)` and `Profile Photo (Recommended: 600 × 600 px · 1:1 Square)`).
- **Interactive Contact & Inquiry Pipeline:**
  - Public contact submissions are saved directly to the `ContactInquiry` database table and surfaced in the admin CMS with unread badges and one-click resolved toggles.

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|:---|:---|:---|
| **Backend** | Python 3.12+, Django 5.2 | High-level web framework, ORM, Auth subsystem |
| **Database** | MySQL (Local via PyMySQL) / SQLite & PostgreSQL (Cloud auto-fallback) | Relational data persistence with dynamic connection adapter |
| **Server & WSGI**| Gunicorn & WhiteNoise | Production-grade WSGI HTTP server & static asset compression |
| **Frontend** | Django Templates, HTML5, Vanilla CSS, Bootstrap Icons | Responsive, accessible, custom design system |
| **Security** | CSRF Tokens, PBKDF2 Password Hashing, Decorator Guards | Enterprise authentication and authorization standards |
| **Deployment** | Render.com | Automated CI/CD pipeline linked to GitHub `main` branch |

---

## 📂 Project Structure

```
Nirmaan_Foundation_Project/
├── manage.py                          <- Django management script
├── build.sh                           <- Render build, collectstatic & migration script
├── requirements.txt                   <- Production and development dependencies
├── .env.example                       <- Environment variable template (secrets excluded)
├── .gitignore                         <- Comprehensive Git exclusions
├── config/                            <- Django core configuration
│   ├── __init__.py                    <- PyMySQL driver patch
│   ├── settings.py                    <- Environment-aware settings (WhiteNoise, DB fallback)
│   ├── urls.py                        <- Root URL routing
│   ├── wsgi.py                        <- WSGI entry point for Gunicorn
│   └── asgi.py                        <- ASGI entry point
├── accounts/                          <- Authentication & user management app
│   ├── models.py                      <- CustomUser & PasswordResetOTP models
│   ├── views.py                       <- Login, register, logout, OTP & dashboard views
│   ├── forms.py                       <- Registration & Authentication forms
│   ├── urls.py                        <- Accounts endpoint routing
│   └── admin.py                       <- Django Admin model registration
├── home/                              <- Public landing page app
│   ├── views.py                       <- Homepage view
│   └── urls.py                        <- Root home route
├── templates/                         <- HTML Templates
│   ├── base.html                      <- Public page shell
│   ├── base_auth.html                 <- 50/50 split authentication layout
│   ├── base_dashboard.html            <- Shared dashboard layout (sidebar + header)
│   ├── accounts/
│   │   ├── login.html                 <- Responsive sign-in page
│   │   ├── register.html              <- Registration with validation
│   │   ├── admin_dashboard.html       <- Admin metrics & user directory
│   │   ├── volunteer_dashboard.html   <- Volunteer portal & drives
│   │   ├── donor_dashboard.html       <- Donor portal & impact
│   │   └── password_reset*.html       <- Multi-step OTP recovery flow
│   └── home/
│       └── index.html                 <- Public homepage & impact showcase
├── static/
│   ├── css/
│   │   ├── auth.css                   <- Auth form styles & visual panel
│   │   ├── dashboard.css              <- Role-tailored dashboard components
│   │   └── home.css                   <- Landing page layout
│   └── images/                        <- Brand logos, hero visuals, illustrations
├── docs/
│   └── assignment-1-authentication.md <- Detailed architecture specification
└── tests/
    └── test_assignment1.py            <- Automated unit and integration test suite
```

---

## ⚙️ Local Development Setup

### 1. Prerequisites
- Python 3.12 or later
- MySQL Server 8.x (or fallback to SQLite)
- Git

### 2. Clone the Repository
```bash
git clone https://github.com/sankettt27/Nirmaan_Foundation_Project.git
cd Nirmaan_Foundation_Project
```

### 3. Create a Virtual Environment & Install Dependencies
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Fill in your local database credentials or leave blank to use the automatic SQLite fallback.

### 5. Run Database Migrations
```bash
python manage.py makemigrations accounts
python manage.py migrate
```

### 6. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 7. Launch Development Server
```bash
python manage.py runserver
```
Navigate to `http://127.0.0.1:8000/` in your browser.

---

## 🚦 Endpoints & Access Control Matrix

### Public Portal & Dedicated Sub-Pages
| Endpoint | Method | Access Level | Description |
|:---|:---:|:---|:---|
| `/` | GET | Public | Dynamic home page with hero slider, vision & mission, stats, and initiatives |
| `/about/` | GET | Public | About Us with interactive milestones timeline, leadership team, and events |
| `/programs/` | GET | Public | Comprehensive initiatives catalog, curriculum highlights, and pedagogy model |
| `/impact/` | GET | Public | Impact metrics, beneficiary transformation case studies, and annual reports |
| `/volunteer/` | GET | Public | 4-step volunteer roadmap, open role listings, and volunteer FAQs |
| `/partner/` | GET | Public | CSR collaboration models, institutional grant tiers, and corporate partner logos |
| `/contact/` | GET, POST | Public | Working contact inquiry form (persists to DB), helplines, and chapter offices |

### Authentication & Role Dashboards
| Endpoint | Method | Access Level | Description |
|:---|:---:|:---|:---|
| `/login/` | GET, POST | Public | User sign-in with automatic role-based dashboard redirection |
| `/register/` | GET, POST | Public | New user sign-up (automatically creates Volunteer role) |
| `/logout/` | POST | Authenticated | Secure session termination and token invalidation |
| `/dashboard/admin/` | GET | Role: `admin` | Platform analytics, user directory, and administrative quick actions |
| `/dashboard/volunteer/`| GET | Role: `volunteer` | Volunteer portal with community drives, badges, and impact hours |
| `/dashboard/donor/` | GET | Role: `donor` | Donor portal with contribution metrics and tax receipts |
| `/password-reset/` | GET, POST | Public | Request password reset email / 6-digit OTP |
| `/password-reset/verify/`| GET, POST | Public | Verify 6-digit OTP code and set new password |

### Admin Content Management System (CMS)
| Endpoint | Method | Access Level | Description |
|:---|:---:|:---|:---|
| `/dashboard/admin/home/` | GET | Role: `admin` | CMS Dashboard overview with section cards & unread inquiry badges |
| `.../home/banners/` | GET, POST | Role: `admin` | Manage hero banners, slider sequencing, and active status |
| `.../home/vision-mission/` | GET, POST | Role: `admin` | Manage vision & mission statement blocks |
| `.../home/statistics/` | GET, POST | Role: `admin` | Manage impact metrics, numeric counters, and icons |
| `.../home/initiatives/` | GET, POST | Role: `admin` | Manage initiatives, tags, and curriculum highlights |
| `/dashboard/admin/team/` | GET, POST | Role: `admin` | Manage leadership team, designations, and photos |
| `/dashboard/admin/milestones/` | GET, POST | Role: `admin` | Manage historical timeline journey milestones |
| `/dashboard/admin/events/` | GET, POST | Role: `admin` | Manage community events, drives, and photo gallery |
| `/dashboard/admin/stories/` | GET, POST | Role: `admin` | Manage student transformation stories and quotes |
| `/dashboard/admin/reports/` | GET, POST | Role: `admin` | Manage annual audited reports and disclosures |
| `/dashboard/admin/opportunities/` | GET, POST | Role: `admin` | Manage open volunteer roles and weekly commitments |
| `/dashboard/admin/partners/` | GET, POST | Role: `admin` | Manage corporate CSR partner logos and endorsements |
| `/dashboard/admin/offices/` | GET, POST | Role: `admin` | Manage chapter offices and contact touchpoints |
| `/dashboard/admin/faqs/` | GET, POST | Role: `admin` | Manage categorized FAQs (accordion) |
| `/dashboard/admin/inquiries/` | GET, POST | Role: `admin` | View inquiries, toggle resolved status, or delete |

---

## 🧪 Automated Testing

Run the full test suite covering authentication, session security, CMS models, public pages, permissions, and CRUD operations:

```bash
# Run both Assignment 1 and Assignment 2 test suites (66 total tests):
python manage.py test tests.test_assignment1 tests.test_assignment2 --settings=config.test_settings -v 1

# Or run Assignment 2 tests exclusively:
python manage.py test tests.test_assignment2 --settings=config.test_settings -v 2
```

---

## 🔒 Security Implementations

1. **Password Hashing:** Passwords are never stored in plaintext; hashed using PBKDF2 with SHA-256 and salt.
2. **CSRF Enforcement:** All forms implement secure CSRF tokens verified on every state-altering POST request.
3. **Privilege Escalation Prevention:** Public registration strictly creates standard accounts (`role='volunteer'`); administrative accounts cannot be self-assigned.
4. **Backend Role Guards:** Access to dashboards and CMS admin endpoints is enforced server-side using `@role_required` decorators, preventing unauthorized URL tampering.
5. **Credential Protection:** Secrets and database connection strings are managed through environment variables and never committed to Git (`.env` strictly excluded).
6. **Session Timeout:** Automatic inactivity timeout after 30 minutes of idle time.
7. **Safe Image Uploads:** User-uploaded assets are isolated and validated in model forms with explicit aspect ratio checks.

---

## 👥 Authors & Acknowledgments

- **Developer:** Sanket Zinjurke
- **Organization:** Nirmaan Foundation
- **Milestones:**
  - Assignment 1 — User Authentication & Registration System (Completed & Verified)
  - Assignment 2 — Home Page Content Management System & Sub-Pages (Completed & Verified)

