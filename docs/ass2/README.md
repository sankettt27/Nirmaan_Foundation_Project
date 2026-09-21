# Nirmaan Foundation — Assignment 2: Home Page Content Management System (CMS) & Sub-Pages

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Render-brightgreen?style=for-the-badge&logo=render)](https://nirmaan-foundation-project.onrender.com/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?style=for-the-badge&logo=github)](https://github.com/sankettt27/Nirmaan_Foundation_Project)
[![Django](https://img.shields.io/badge/Django-5.2-darkgreen?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/Tests-24%2F24%20Passing-success?style=for-the-badge&logo=pytest)](https://github.com/sankettt27/Nirmaan_Foundation_Project)

A complete, production-grade **Content Management System (CMS)** built on top of Django for the **Nirmaan Foundation** NGO web platform. It empowers non-technical administrators to dynamically manage all public-facing media, statistics, statements, initiatives, and sub-page content in real time without touching code or redeploying.

---

## 🚀 Live Demonstration & Access Credentials

- **Public Home Page:** [https://nirmaan-foundation-project.onrender.com/](https://nirmaan-foundation-project.onrender.com/)
- **Admin CMS Dashboard:** [https://nirmaan-foundation-project.onrender.com/dashboard/admin/home/](https://nirmaan-foundation-project.onrender.com/dashboard/admin/home/)
- **GitHub Repository:** [https://github.com/sankettt27/Nirmaan_Foundation_Project](https://github.com/sankettt27/Nirmaan_Foundation_Project)

### 🔑 Administrator Test Credentials

| Role | Email | Password | Destination Dashboard |
|:---|:---|:---|:---|
| **System Administrator** | `admin@nirmaan.org` | `Admin@123` | `/dashboard/admin/home/` |
| **Standard User / Volunteer** | Any account created at `/register/` | Your choice | Redirected / Blocked from CMS |

---

## 📋 Assignment 2 Requirements & Implementation

### 1. Core Home Page CMS Modules (`/dashboard/admin/home/`)
- **Hero Image Slider / Banners Management:**
  - Add, edit, reorder, soft-delete/publish toggle, and delete banner slides.
  - Controls title, subtitle, CTA button text, and CTA destination URL.
- **Vision & Mission Section Management:**
  - Manage individual vision and mission statement cards.
  - Customizable Bootstrap icon selector and display sequencing.
- **Impact Statistics Management:**
  - Dynamic numeric counter values (e.g. `30K+`, `150+`, `18+`), labels, and icons.
  - Soft-delete toggle (`is_active`) to hide/show metrics without deleting historical records.
- **Our Initiatives / Programs Management:**
  - Manage initiative cards, category tags (e.g. `In Schools`, `STEM & Digital`), short descriptions, curriculum focus, and beneficiaries reached.

---

### 2. Dedicated Public Sub-Pages (Bhumi.ngo-Inspired)
In addition to the home page, 6 dedicated sub-pages have been engineered and linked across the platform:

1. **About Us (`/about/`):**
   - Interactive milestone journey timeline (`AboutMilestone`).
   - Executive leadership and advisory board directory (`TeamMember`).
   - Community drives and events photo gallery (`AboutEvent`).
2. **Programs (`/programs/`):**
   - Comprehensive initiatives catalog with category filtering.
   - 4-pillar pedagogical framework and curriculum highlights.
   - Program-specific FAQ accordion.
3. **Impact (`/impact/`):**
   - Decadal transformation metrics and statistics counters.
   - Real-world student and community beneficiary case studies (`ImpactStory`).
   - Audited annual reports and statutory compliance disclosures (`AnnualReport`).
4. **Volunteer (`/volunteer/`):**
   - 4-step volunteer onboarding roadmap.
   - Open teaching, mentoring, and digital volunteer opportunities (`VolunteerOpportunity`).
   - Volunteer FAQ accordion and registration CTA.
5. **Partner With Us (`/partner/`):**
   - Turnkey corporate CSR models, school adoption packages, and 80G tax benefits.
   - Corporate partner logo wall and testimonials (`PartnerOrganization`).
   - CSR inquiry trigger.
6. **Contact Us (`/contact/`):**
   - Working message inquiry form that **persists directly into the database** (`ContactInquiry`).
   - National Headquarters and chapter office cards (`OfficeLocation`).
   - Central helplines and categorized FAQs.

---

### 3. Image Display Ratio Guidance in Brackets
To prevent blurry, stretched, or mismatched imagery uploaded by administrators, **every CMS image field explicitly specifies optimal pixel dimensions and aspect ratios directly in the form label**:

| CMS Section | Recommended Dimensions | Display Aspect Ratio | Form Label Display |
|:---|:---:|:---:|:---|
| **Hero Banners** | `1920 × 800 px` | 16:9 widescreen | `Banner Image (Recommended: 1920 × 800 px · 16:9 ratio)` |
| **Initiatives / Programs** | `800 × 500 px` | 16:10 landscape | `Program Image (Recommended: 800 × 500 px · 16:10 ratio)` |
| **Team Profiles** | `600 × 600 px` | 1:1 square | `Profile Photo (Recommended: 600 × 600 px · 1:1 Square)` |
| **Impact Beneficiaries** | `600 × 600 px` | 1:1 square | `Beneficiary Photo (Recommended: 600 × 600 px · 1:1 Square)` |
| **Events & Drives** | `800 × 550 px` | 16:11 landscape | `Event Cover Image (Recommended: 800 × 550 px · 16:11 ratio)` |
| **Annual Report Covers** | `600 × 850 px` | 3:4 portrait (A4) | `Report Cover Image (Recommended: 600 × 850 px · 3:4 Portrait / A4)` |
| **Partner Logos** | `400 × 400 px` | 1:1 square (PNG) | `Organization Logo (Recommended: 400 × 400 px · 1:1 Square, PNG Transparent)` |

---

### 4. Interactive Contact & Inquiry Pipeline
- When a public visitor submits a message on `/contact/`, the backend validates and stores the record in the `ContactInquiry` table.
- The Admin CMS dashboard features a **live pending inquiry counter** and an inquiry triage table (`/dashboard/admin/inquiries/`).
- Administrators can review inquiries, toggle `is_resolved` status with a single click, or delete spam inquiries.

---

## 🗄️ Database Architecture (14 Relational Models)

All CMS models are defined in `cms/models.py` with `order` sequencing, `is_active` publishing flags, and audit timestamps.

```
Nirmaan Foundation CMS Schema
├── Core Home Models
│   ├── Banner                 (Hero slider images, headlines, CTA links)
│   ├── VisionMission          (Vision and mission statement blocks & icons)
│   ├── Statistic              (Impact counters, labels, icons, soft-delete)
│   └── Initiative             (Programs showcase, categories, curriculum)
├── About Us Models
│   ├── AboutMilestone         (Journey timeline milestones by year)
│   ├── TeamMember             (Leadership team, advisory board, photos)
│   └── AboutEvent             (Recent community events & photo gallery)
├── Impact Models
│   ├── ImpactStory            (Beneficiary transformation stories & quotes)
│   └── AnnualReport           (Audited reports, fiscal years, PDF URLs)
├── Engagement Models
│   ├── VolunteerOpportunity   (Open volunteer roles, weekly commitments)
│   └── PartnerOrganization    (Corporate CSR partners, logos, endorsements)
└── Contact & Support Models
    ├── OfficeLocation         (Chapter offices, addresses, contact info)
    ├── FAQ                    (Categorized accordion FAQs)
    └── ContactInquiry         (Visitor messages, email, status toggle)
```

---

## 🔒 Security & Authorization

1. **Role-Based Access Control (RBAC):**
   - All CMS views are protected with the custom `@role_required('admin')` decorator.
   - Anonymous visitors are redirected to `/login/`.
   - Logged-in volunteers or donors attempting to access CMS URLs receive an access denied redirect.
2. **CSRF Enforcement:**
   - Every CMS form and state-altering POST request enforces Django CSRF verification tokens.
3. **Soft-Delete Architecture:**
   - Deactivating an item (`is_active=False`) instantly hides it from public view while keeping audit history intact.
4. **Media Isolation:**
   - Uploaded files are segregated into isolated namespaces under `media/cms/` (`banners/`, `initiatives/`, `team/`, `events/`, `reports/`, `partners/`).

---

## 🚦 Endpoints & Routes Matrix

### Public Pages
| Route | Method | Description |
|:---|:---:|:---|
| `/` | GET | Dynamic home page with hero slider, vision & mission, stats, and initiatives |
| `/about/` | GET | About Us with milestones timeline, leadership team, and events gallery |
| `/programs/` | GET | Comprehensive initiatives catalog, curriculum highlights, and pedagogy model |
| `/impact/` | GET | Impact metrics, beneficiary transformation case studies, and annual reports |
| `/volunteer/` | GET | 4-step volunteer roadmap, open role listings, and volunteer FAQs |
| `/partner/` | GET | CSR collaboration models, institutional grant tiers, and corporate partner logos |
| `/contact/` | GET, POST | Contact inquiry form (persists to DB), helplines, and chapter offices |

### Admin CMS Endpoints (`/dashboard/admin/home/`)
| Section | List Route | Create Route | Edit Route | Delete Route |
|:---|:---|:---|:---|:---|
| **Overview** | `/dashboard/admin/home/` | — | — | — |
| **Hero Banners** | `.../banners/` | `.../banners/add/` | `.../banners/<id>/edit/` | `.../banners/<id>/delete/` |
| **Vision & Mission** | `.../vision-mission/` | `.../vision-mission/add/` | `.../vision-mission/<id>/edit/` | `.../vision-mission/<id>/delete/` |
| **Statistics** | `.../statistics/` | `.../statistics/add/` | `.../statistics/<id>/edit/` | `.../statistics/<id>/delete/` |
| **Initiatives** | `.../initiatives/` | `.../initiatives/add/` | `.../initiatives/<id>/edit/` | `.../initiatives/<id>/delete/` |
| **Leadership Team** | `/dashboard/admin/team/` | `/dashboard/admin/team/add/` | `/dashboard/admin/team/<id>/edit/` | `/dashboard/admin/team/<id>/delete/` |
| **Milestones** | `/dashboard/admin/milestones/` | `/dashboard/admin/milestones/add/` | `/dashboard/admin/milestones/<id>/edit/` | `/dashboard/admin/milestones/<id>/delete/` |
| **Events & Drives** | `/dashboard/admin/events/` | `/dashboard/admin/events/add/` | `/dashboard/admin/events/<id>/edit/` | `/dashboard/admin/events/<id>/delete/` |
| **Impact Stories** | `/dashboard/admin/stories/` | `/dashboard/admin/stories/add/` | `/dashboard/admin/stories/<id>/edit/` | `/dashboard/admin/stories/<id>/delete/` |
| **Annual Reports** | `/dashboard/admin/reports/` | `/dashboard/admin/reports/add/` | `/dashboard/admin/reports/<id>/edit/` | `/dashboard/admin/reports/<id>/delete/` |
| **Volunteer Roles** | `/dashboard/admin/opportunities/` | `/dashboard/admin/opportunities/add/` | `/dashboard/admin/opportunities/<id>/edit/` | `/dashboard/admin/opportunities/<id>/delete/` |
| **Corporate Partners**| `/dashboard/admin/partners/` | `/dashboard/admin/partners/add/` | `/dashboard/admin/partners/<id>/edit/` | `/dashboard/admin/partners/<id>/delete/` |
| **Chapter Offices** | `/dashboard/admin/offices/` | `/dashboard/admin/offices/add/` | `/dashboard/admin/offices/<id>/edit/` | `/dashboard/admin/offices/<id>/delete/` |
| **Accordion FAQs** | `/dashboard/admin/faqs/` | `/dashboard/admin/faqs/add/` | `/dashboard/admin/faqs/<id>/edit/` | `/dashboard/admin/faqs/<id>/delete/` |
| **Contact Inquiries**| `/dashboard/admin/inquiries/` | — | `.../<id>/toggle-resolved/` | `.../<id>/delete/` |

---

## 🧪 Automated Testing & Verification

The dedicated test suite in `tests/test_assignment2.py` includes **24 automated unit and integration tests**:

1. **`CMSModelTests`:** Creation, default active states, and string representations across all 14 models.
2. **`PublicPagesViewTests`:** HTTP 200 responses and CMS context delivery across all public routes.
3. **`CMSVisibilityFilterTests`:** Confirmation that inactive items are withheld from public view.
4. **`ContactInquirySubmissionTests`:** Validates form validation, database storage, and error handling.
5. **`CMSAccessControlTests`:** Validates that anonymous users and volunteers are blocked from CMS admin endpoints.
6. **`CMSCrudWorkflowTests`:** Full create, update, delete, and toggle workflows for administrative operations.

### Run Assignment 2 Tests:
```bash
python manage.py test tests.test_assignment2 --settings=config.test_settings -v 2
```

### Run Full Test Suite (Assignment 1 + Assignment 2):
```bash
python manage.py test tests.test_assignment1 tests.test_assignment2 --settings=config.test_settings -v 1
```

**Verification Output:**
```
Ran 24 tests in 3.625s
OK (0 failures, 0 errors)
```

---

## 💻 Local Setup & Execution Guide

### 1. Prerequisites
- Python 3.12 or higher
- MySQL Server (or SQLite fallback)
- Git

### 2. Clone the Repository
```bash
git clone https://github.com/sankettt27/Nirmaan_Foundation_Project.git
cd Nirmaan_Foundation_Project
```

### 3. Create & Activate Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
*(Leave DB credentials empty to use the automatic SQLite fallback, or configure your local MySQL).*

### 6. Apply Migrations
```bash
python manage.py migrate
```

### 7. Run the Development Server
```bash
python manage.py runserver
```
Navigate to `http://127.0.0.1:8000/` in your browser.

---

## 👥 Authors & Project Metadata

- **Developer:** Sanket Zinjurke
- **Organization:** Nirmaan Foundation
- **Milestone:** Assignment 2 — Home Page Content Management System & Sub-Pages
- **Completion Status:** 100% Completed, Verified, and Deployed
