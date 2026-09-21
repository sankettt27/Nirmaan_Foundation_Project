# Assignment 2 — Home Page Content Management System (CMS) & Sub-Pages

**Project:** Nirmaan Foundation — NGO Content Management Platform  
**Assignment:** 2 of ongoing internship  
**Status:** 100% Implemented, Tested, and Deployed  
**Live Application:** [https://nirmaan-foundation-project.onrender.com/](https://nirmaan-foundation-project.onrender.com/)  

---

## 1. Objective

Design, engineer, and deploy a production-ready **Content Management System (CMS)** for the Nirmaan Foundation platform that empowers non-technical administrators to manage all public-facing content dynamically without code changes or redeployments.

In addition to the core home page sections (Hero Slider, Vision & Mission, Statistics, Initiatives), this implementation delivers 6 dedicated, content-rich public sub-pages inspired by modern non-profit platforms like **Bhumi.ngo**:
1. **About Us (`/about/`)** — Organizational timeline, executive leadership, and events gallery.
2. **Programs (`/programs/`)** — Flagship educational initiatives, pedagogy model, and program FAQs.
3. **Impact (`/impact/`)** — Verified social metrics, beneficiary transformation stories, and audited annual reports.
4. **Volunteer (`/volunteer/`)** — 4-step volunteer roadmap, open teaching/mentoring opportunities, and volunteer FAQs.
5. **Partner With Us (`/partner/`)** — Turnkey CSR models, institutional grant tiers, and corporate partner logos.
6. **Contact Us (`/contact/`)** — Interactive inquiry submission form, central helplines, and chapter offices.

---

## 2. Technology Stack

| Layer | Technology | Purpose |
|:---|:---|:---|
| **Backend** | Python 3.12+, Django 5.2 | High-level MVC/MVT web framework, ORM, Forms, and Decorators |
| **Database** | MySQL (PyMySQL) / SQLite (Test/Cloud fallback) | Relational database schema with transactional integrity |
| **Frontend** | Django Templates, HTML5, Vanilla CSS | Bespoke, accessible design system with glassmorphism & cards |
| **Icons & Media** | Bootstrap Icons, Responsive Images | Visual taxonomy, retina-ready displays, aspect-ratio enforcement |
| **Access Control** | Custom `@role_required('admin')` decorator | Strict role-based isolation of CMS admin interfaces |
| **Testing** | Django TestCase (`tests/test_assignment2.py`) | 24 automated unit and integration tests |

---

## 3. Database Architecture & Schema

The CMS is backed by 14 relational models in the `cms` Django app. All models incorporate `order` for admin-controlled display sequence, `is_active` for soft-delete/draft state, and audit timestamps.

### 3.1 Core Home Page Tables

```
+-------------------------------------------------------------+
|                         banners                             |
+-------------------+------------------+----------------------+
| Field             | Type             | Description          |
+-------------------+------------------+----------------------+
| id                | INT (PK)         | Unique identifier    |
| title             | VARCHAR(200)     | Banner headline      |
| subtitle          | TEXT             | Supporting text      |
| image             | VARCHAR(255)     | Banner visual file   |
| button_text       | VARCHAR(50)      | CTA label            |
| button_link       | VARCHAR(300)     | CTA destination URL  |
| order             | INT UNSIGNED     | Display order        |
| is_active         | BOOLEAN          | Publish/draft toggle |
| created_at        | DATETIME         | Creation timestamp   |
| updated_at        | DATETIME         | Last update          |
+-------------------+------------------+----------------------+

+-------------------------------------------------------------+
|                     vision_mission                          |
+-------------------+------------------+----------------------+
| Field             | Type             | Description          |
+-------------------+------------------+----------------------+
| id                | INT (PK)         | Unique identifier    |
| section_type      | VARCHAR(10)      | 'vision' | 'mission' |
| title             | VARCHAR(200)     | Section heading      |
| content           | TEXT             | Statement body       |
| icon              | VARCHAR(50)      | Bootstrap Icon class |
| order             | INT UNSIGNED     | Display order        |
| is_active         | BOOLEAN          | Publish/draft toggle |
| updated_at        | DATETIME         | Last update          |
+-------------------+------------------+----------------------+

+-------------------------------------------------------------+
|                        statistic                            |
+-------------------+------------------+----------------------+
| Field             | Type             | Description          |
+-------------------+------------------+----------------------+
| id                | INT (PK)         | Unique identifier    |
| label             | VARCHAR(100)     | Metric title         |
| value             | VARCHAR(50)      | e.g., "30K+", "18+"  |
| icon              | VARCHAR(50)      | Bootstrap Icon class |
| order             | INT UNSIGNED     | Display order        |
| is_active         | BOOLEAN          | Publish/draft toggle |
+-------------------+------------------+----------------------+

+-------------------------------------------------------------+
|                       initiatives                           |
+-------------------+------------------+----------------------+
| Field             | Type             | Description          |
+-------------------+------------------+----------------------+
| id                | INT (PK)         | Unique identifier    |
| title             | VARCHAR(200)     | Program name         |
| tag               | VARCHAR(50)      | e.g. "In Schools"    |
| description       | TEXT             | Short summary card   |
| image             | VARCHAR(255)     | Cover image file     |
| link              | VARCHAR(300)     | Destination link     |
| detailed_content  | TEXT             | In-depth description |
| key_features      | TEXT             | Bullet points        |
| curriculum_highlight VARCHAR(200)    | Pedagogical focus    |
| beneficiaries_reached VARCHAR(50)    | e.g. "15,000+ Kids"  |
| order             | INT UNSIGNED     | Display order        |
| is_active         | BOOLEAN          | Publish/draft toggle |
+-------------------+------------------+----------------------+
```

### 3.2 Extended Subpage Models

| Model | Table Name | Purpose | Key Fields |
|:---|:---|:---|:---|
| **AboutMilestone** | `cms_about_milestone` | Journey roadmap timeline | `year`, `title`, `description`, `icon`, `order` |
| **TeamMember** | `cms_team_member` | Leadership & advisory board | `name`, `role`, `category`, `bio`, `photo`, `linkedin_url` |
| **AboutEvent** | `cms_about_event` | Community drives & gallery | `title`, `category`, `event_date`, `location`, `image` |
| **ImpactStory** | `cms_impact_story` | Beneficiary case studies | `name`, `role_or_school`, `location`, `quote`, `story`, `photo` |
| **AnnualReport** | `cms_annual_report` | Audited financial disclosures| `title`, `fiscal_year`, `summary`, `file_url`, `cover_image` |
| **VolunteerOpportunity** | `cms_volunteer_opportunity` | Open volunteer roles | `title`, `category`, `commitment`, `description`, `skills_needed` |
| **PartnerOrganization** | `cms_partner_organization` | Corporate CSR partners | `name`, `category`, `logo`, `website_url`, `testimonial` |
| **OfficeLocation** | `cms_office_location` | Chapter offices | `city`, `is_hq`, `address`, `email`, `phone`, `order` |
| **FAQ** | `cms_faq` | Accordion FAQs | `category` (general/programs/volunteer/partner), `question`, `answer` |
| **ContactInquiry** | `cms_contact_inquiry` | User contact messages | `name`, `email`, `phone`, `category`, `subject`, `message`, `is_resolved` |

---

## 4. Admin Image Dimension & Ratio Guidance

To eliminate blurry or distorted imagery on the public portal, all Django CMS forms explicitly display **recommended pixel dimensions and aspect ratios directly in the form label brackets**:

| Section | Recommended Resolution | Aspect Ratio | Form Label Display |
|:---|:---:|:---:|:---|
| **Hero Banners** | `1920 × 800 px` | 16:9 widescreen | `Banner Image (Recommended: 1920 × 800 px · 16:9 ratio)` |
| **Initiatives / Programs** | `800 × 500 px` | 16:10 landscape | `Program Image (Recommended: 800 × 500 px · 16:10 ratio)` |
| **Team Profiles** | `600 × 600 px` | 1:1 square | `Profile Photo (Recommended: 600 × 600 px · 1:1 Square)` |
| **Impact Beneficiaries** | `600 × 600 px` | 1:1 square | `Beneficiary Photo (Recommended: 600 × 600 px · 1:1 Square)` |
| **Events & Drives** | `800 × 550 px` | 16:11 landscape | `Event Cover Image (Recommended: 800 × 550 px · 16:11 ratio)` |
| **Annual Report Covers** | `600 × 850 px` | 3:4 portrait (A4) | `Report Cover Image (Recommended: 600 × 850 px · 3:4 Portrait / A4)` |
| **Partner Logos** | `400 × 400 px` | 1:1 square (PNG) | `Organization Logo (Recommended: 400 × 400 px · 1:1 Square, PNG Transparent)` |

Form fields render this guidance through `.cms-size-hint` badges styled directly in `static/css/cms.css`.

---

## 5. Security & Access Control

1. **Authentication Enforcement:**
   Every CMS endpoint is guarded by the custom `@role_required('admin')` decorator. Anonymous visitors are redirected to `/login/`, while authenticated non-admin users (volunteers, donors) are denied access and redirected.
2. **CSRF Protection:**
   All create, update, toggle, and delete forms require valid CSRF tokens (`{% csrf_token %}`).
3. **Safe File Uploads:**
   Image fields store assets in dedicated namespaces under `media/cms/` (`banners/`, `initiatives/`, `team/`, `events/`, `reports/`, `partners/`).
4. **Soft Delete / Publishing Control:**
   Every CMS model features an `is_active` boolean field. Toggling `is_active=False` removes content from public consumption immediately without deleting audit trails.

---

## 6. Public Pages & Routing Matrix

| Route | View Function | Template | Content Delivered |
|:---|:---|:---|:---|
| `/` | `home.views.index` | `templates/home/index.html` | Hero slider, Vision & Mission cards, Counter stats, Initiative grid, Testimonial ticker |
| `/about/` | `home.views.about_view` | `templates/home/about.html` | Organizational story, Timeline milestone cards, Leadership team, Recent events gallery |
| `/programs/` | `home.views.programs_view` | `templates/home/programs.html` | Complete program catalog, Curriculum highlights, Pedagogy framework, Program FAQs |
| `/impact/` | `home.views.impact_view` | `templates/home/impact.html` | Impact statistics, Beneficiary stories with photos, Audited annual reports, Compliance disclosures |
| `/volunteer/` | `home.views.volunteer_view` | `templates/home/volunteer.html` | 4-step volunteer roadmap, Open teaching & mentoring opportunities, Volunteer FAQs, Sign-up CTA |
| `/partner/` | `home.views.partner_view` | `templates/home/partner.html` | Corporate CSR models, Institutional grant alignment, Partner logo wall, CSR inquiry trigger |
| `/contact/` | `home.views.contact_view` | `templates/home/contact.html` | Working message submission form (persists to `ContactInquiry`), Central helplines, Chapter offices |

---

## 7. Admin CMS Endpoints Matrix

Base URL: `/dashboard/admin/home/`

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
| **Volunteer Roles** | `/dashboard/admin/opportunities/`| `/dashboard/admin/opportunities/add/` | `/dashboard/admin/opportunities/<id>/edit/` | `/dashboard/admin/opportunities/<id>/delete/` |
| **Corporate Partners**| `/dashboard/admin/partners/` | `/dashboard/admin/partners/add/` | `/dashboard/admin/partners/<id>/edit/` | `/dashboard/admin/partners/<id>/delete/` |
| **Chapter Offices** | `/dashboard/admin/offices/` | `/dashboard/admin/offices/add/` | `/dashboard/admin/offices/<id>/edit/` | `/dashboard/admin/offices/<id>/delete/` |
| **Accordion FAQs** | `/dashboard/admin/faqs/` | `/dashboard/admin/faqs/add/` | `/dashboard/admin/faqs/<id>/edit/` | `/dashboard/admin/faqs/<id>/delete/` |
| **Contact Inquiries**| `/dashboard/admin/inquiries/` | — | `.../<id>/toggle-resolved/` | `.../<id>/delete/` |

---

## 8. Verification & Automated Testing

The automated test suite in `tests/test_assignment2.py` validates all Assignment 2 functionality across 6 test classes:

1. `CMSModelTests` — Model creation, defaults, and string representations across all 14 models.
2. `PublicPagesViewTests` — HTTP 200 response and correct context rendering for all 7 public views.
3. `CMSVisibilityFilterTests` — Confirmation that draft items (`is_active=False`) are never visible to public visitors.
4. `ContactInquirySubmissionTests` — Form validation, data persistence, and error handling.
5. `CMSAccessControlTests` — Role enforcement (anonymous visitors and regular volunteers blocked from admin CMS).
6. `CMSCrudWorkflowTests` — Create, edit, soft-delete, and status toggle operations.

### Running the Test Suite:

```bash
# Run Assignment 2 tests exclusively
python manage.py test tests.test_assignment2 --settings=config.test_settings -v 2

# Run combined Assignment 1 & 2 test suites (66 total tests)
python manage.py test tests.test_assignment1 tests.test_assignment2 --settings=config.test_settings -v 1
```

**Test Execution Results:**
```
Ran 66 tests in 21.965s
OK
```
