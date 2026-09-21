"""
tests/test_assignment2.py — Comprehensive Test Suite for Assignment 2.

Nirmaan Foundation — Home Page Content Management System (CMS) & Sub-Pages

Test Coverage:
  1. CMS Model Integrity & Default States (All 14 CMS models)
  2. Public Sub-Pages Rendering & CMS Context Delivery (/, /about/, /programs/, /impact/, /volunteer/, /partner/, /contact/)
  3. Active Status Visibility (Inactive CMS items are omitted from public pages)
  4. Contact Inquiry Form Submissions (Validation, persistence, error handling)
  5. CMS Admin Role-Based Access Control (Anonymous & Volunteer blocked; Admin granted)
  6. CMS Admin CRUD Workflows (Create, update, toggle active, resolve inquiries, delete)

Run with:
    python manage.py test tests.test_assignment2 --settings=config.test_settings
"""

from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import CustomUser
from cms.models import (
    Banner,
    VisionMission,
    Statistic,
    Initiative,
    AboutMilestone,
    TeamMember,
    AboutEvent,
    ImpactStory,
    AnnualReport,
    VolunteerOpportunity,
    PartnerOrganization,
    OfficeLocation,
    FAQ,
    ContactInquiry,
)


# ─────────────────────────────────────────────────────────────
# TEST FIXTURES & HELPERS
# ─────────────────────────────────────────────────────────────

def create_admin_user(email='admin@nirmaan.org', password='AdminPassword123!'):
    """Helper to create a verified administrator account."""
    return CustomUser.objects.create_user(
        email=email,
        full_name='System Admin',
        password=password,
        role='admin',
        status='active',
    )


def create_volunteer_user(email='volunteer@nirmaan.org', password='VolunteerPass123!'):
    """Helper to create a standard volunteer / public user account."""
    return CustomUser.objects.create_user(
        email=email,
        full_name='Aarav Sharma',
        password=password,
        role='user',
        status='active',
    )


# ─────────────────────────────────────────────────────────────
# 1. CMS MODELS & DATABASE INTEGRITY TESTS
# ─────────────────────────────────────────────────────────────

class CMSModelTests(TestCase):
    """Verifies that all CMS models instantiate, persist, and stringify properly."""

    def test_banner_creation_and_str(self):
        """Banner model stores attributes and has correct active indicator in str."""
        banner = Banner.objects.create(
            title='Empowering Every Child Through Education',
            subtitle='Join our journey to bring classroom education to remote areas.',
            button_text='Explore Programs',
            button_link='/programs/',
            order=1,
            is_active=True,
        )
        self.assertIn('Empowering Every Child Through Education', str(banner))
        self.assertTrue(banner.is_active)
        self.assertEqual(banner.order, 1)

    def test_vision_mission_creation_and_str(self):
        """VisionMission model holds individual vision and mission statements."""
        vm = VisionMission.objects.create(
            section_type='vision',
            title='Our Vision',
            content='An equitable India where every child achieves potential.',
            icon='bi-eye-fill',
            is_active=True,
        )
        self.assertIn('Our Vision', str(vm))
        self.assertTrue(vm.is_active)

    def test_statistic_creation_and_str(self):
        """Statistic model stores impact counter metrics."""
        stat = Statistic.objects.create(
            label='Children Educated',
            value='25,000+',
            icon='bi-people-fill',
            order=1,
            is_active=True,
        )
        self.assertIn('Children Educated', str(stat))
        self.assertIn('25,000+', str(stat))

    def test_initiative_creation_and_str(self):
        """Initiative model stores educational projects and tags."""
        init = Initiative.objects.create(
            title='Ignite Literacy Drive',
            tag='In Schools',
            description='Weekend accelerated reading circles for primary grades.',
            order=1,
            is_active=True,
        )
        self.assertIn('Ignite Literacy Drive', str(init))
        self.assertEqual(init.tag, 'In Schools')

    def test_extended_models_creation(self):
        """Verifies team members, milestones, stories, and contact inquiries."""
        milestone = AboutMilestone.objects.create(
            year='2015',
            title='Foundation Established',
            description='Started with 2 learning centers in Bengaluru',
            order=1,
        )
        self.assertIn('Foundation Established', str(milestone))

        team = TeamMember.objects.create(name='Priya Patel', role='Founder & Executive Director', order=1)
        self.assertEqual(str(team), 'Priya Patel (Founder & Executive Director)')

        story = ImpactStory.objects.create(
            name='Ananya Sen',
            role_or_school='Grade 10 Scholar',
            location='Bengaluru',
            quote='Nirmaan transformed my perspective.',
            story='Ananya secured admission to top pre-university college.',
            order=1,
        )
        self.assertEqual(str(story), 'Ananya Sen — Bengaluru')

        inquiry = ContactInquiry.objects.create(
            name='Rohan Mehta',
            email='rohan@example.com',
            subject='CSR Collaboration Inquiry',
            message='We would like to partner for our FY26 CSR initiative.',
        )
        self.assertFalse(inquiry.is_resolved)
        self.assertIn('Rohan Mehta', str(inquiry))


# ─────────────────────────────────────────────────────────────
# 2. PUBLIC PAGES ACCESSIBILITY & CMS DATA DELIVERY
# ─────────────────────────────────────────────────────────────

class PublicPagesViewTests(TestCase):
    """Verifies that all public pages render HTTP 200 and surface CMS data."""

    def setUp(self):
        self.client = Client()
        # Seed test CMS data
        self.banner = Banner.objects.create(
            title='Featured Banner Title',
            subtitle='Transforming grassroot learning',
            order=1,
            is_active=True,
        )
        self.stat = Statistic.objects.create(
            label='Schools Partnered',
            value='150+',
            order=1,
            is_active=True,
        )
        self.init = Initiative.objects.create(
            title='STEM for Rural Girls',
            tag='STEM & Digital',
            description='Hands-on robotics and coding labs.',
            order=1,
            is_active=True,
        )

    def test_home_page_loads_and_displays_cms_content(self):
        """Home page / returns 200 and includes active banners and statistics."""
        response = self.client.get(reverse('home:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Featured Banner Title')
        self.assertContains(response, 'Schools Partnered')
        self.assertContains(response, 'STEM for Rural Girls')

    def test_about_page_loads(self):
        """About page /about/ returns 200 with journey and leadership sections."""
        AboutMilestone.objects.create(
            year='2020',
            title='Reached 10,000 Students',
            description='Expanded footprint across 4 states',
            order=1,
            is_active=True,
        )
        TeamMember.objects.create(name='Dr. Neha Verma', role='Director of Pedagogy', order=1, is_active=True)
        response = self.client.get(reverse('home:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Reached 10,000 Students')
        self.assertContains(response, 'Dr. Neha Verma')

    def test_programs_page_loads(self):
        """Programs page /programs/ returns 200 with initiatives catalog."""
        response = self.client.get(reverse('home:programs'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'STEM for Rural Girls')

    def test_impact_page_loads(self):
        """Impact page /impact/ returns 200 with metrics and reports."""
        ImpactStory.objects.create(
            name='Kavita Sharma',
            role_or_school='Government High School',
            location='Pune',
            quote='I learned to code with confidence.',
            story='Kavita joined our computer literacy circle in 2021.',
            is_active=True,
        )
        response = self.client.get(reverse('home:impact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Kavita Sharma')

    def test_volunteer_page_loads(self):
        """Volunteer page /volunteer/ returns 200 with open volunteer roles."""
        VolunteerOpportunity.objects.create(
            title='Weekend English Tutor',
            commitment='4 hrs / week',
            is_active=True,
        )
        response = self.client.get(reverse('home:volunteer'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Weekend English Tutor')

    def test_partner_page_loads(self):
        """Partner page /partner/ returns 200 with corporate CSR tiers."""
        PartnerOrganization.objects.create(
            name='Tata Consultancy Services',
            category='corporate',
            is_active=True,
        )
        response = self.client.get(reverse('home:partner'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tata Consultancy Services')

    def test_contact_page_loads(self):
        """Contact page /contact/ returns 200 with offices and inquiry form."""
        OfficeLocation.objects.create(
            city='Bengaluru',
            address='100 Feet Road, Indiranagar',
            phone='+91 80 4123 4567',
            is_active=True,
        )
        response = self.client.get(reverse('home:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bengaluru')
        self.assertContains(response, 'Send Inquiry')


# ─────────────────────────────────────────────────────────────
# 3. ACTIVE STATUS & VISIBILITY FILTERING
# ─────────────────────────────────────────────────────────────

class CMSVisibilityFilterTests(TestCase):
    """Ensures draft/inactive items are withheld from public visitors."""

    def setUp(self):
        self.client = Client()

    def test_inactive_banner_is_hidden_from_home(self):
        """Banners with is_active=False must not appear on public home."""
        Banner.objects.create(
            title='Hidden Draft Banner',
            is_active=False,
        )
        response = self.client.get(reverse('home:index'))
        self.assertNotContains(response, 'Hidden Draft Banner')

    def test_inactive_initiative_is_hidden_from_programs(self):
        """Initiatives with is_active=False must not appear on public programs."""
        Initiative.objects.create(
            title='Archived Initiative Alpha',
            tag='Health',
            description='Archived healthcare pilot program',
            is_active=False,
        )
        response = self.client.get(reverse('home:programs'))
        self.assertNotContains(response, 'Archived Initiative Alpha')


# ─────────────────────────────────────────────────────────────
# 4. CONTACT INQUIRY FORM SUBMISSION TESTS
# ─────────────────────────────────────────────────────────────

class ContactInquirySubmissionTests(TestCase):
    """Tests the public contact form validation and persistence."""

    def setUp(self):
        self.client = Client()
        self.contact_url = reverse('home:contact')

    def test_valid_inquiry_submission_creates_record(self):
        """Valid POST creates ContactInquiry record in database with unread state."""
        payload = {
            'name': 'Deepak Verma',
            'email': 'deepak@techcorp.com',
            'phone': '+91 98765 43210',
            'category': 'partner',
            'subject': 'CSR Sponsorship for Karnataka Schools',
            'message': 'We would like to schedule a call to sponsor 5 schools.',
        }
        response = self.client.post(self.contact_url, payload, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ContactInquiry.objects.filter(email='deepak@techcorp.com').exists())

        inquiry = ContactInquiry.objects.get(email='deepak@techcorp.com')
        self.assertEqual(inquiry.name, 'Deepak Verma')
        self.assertEqual(inquiry.category, 'partner')
        self.assertFalse(inquiry.is_resolved)

    def test_incomplete_inquiry_fails_gracefully(self):
        """POST missing name or email does NOT create record and presents validation notice."""
        initial_count = ContactInquiry.objects.count()
        payload = {
            'name': '',
            'email': '',
            'message': 'Hello',
        }
        response = self.client.post(self.contact_url, payload)
        self.assertEqual(ContactInquiry.objects.count(), initial_count)
        self.assertContains(response, 'Please provide your name, email, and message.')


# ─────────────────────────────────────────────────────────────
# 5. CMS ADMIN ACCESS CONTROL & ROLE GUARDS
# ─────────────────────────────────────────────────────────────

class CMSAccessControlTests(TestCase):
    """Verifies strict role-based barriers preventing non-admins from CMS endpoints."""

    def setUp(self):
        self.client = Client()
        self.admin_user = create_admin_user()
        self.volunteer_user = create_volunteer_user()
        self.cms_dash_url = reverse('cms:cms_dashboard')
        self.banner_list_url = reverse('cms:banner_list')
        self.banner_add_url = reverse('cms:banner_create')

    def test_anonymous_user_redirected_to_login(self):
        """Anonymous visitor accessing CMS is redirected to login page."""
        response = self.client.get(self.cms_dash_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_volunteer_user_forbidden_from_cms(self):
        """Standard volunteer user accessing CMS is blocked and redirected."""
        self.client.force_login(self.volunteer_user)
        response = self.client.get(self.cms_dash_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_admin_user_granted_access_to_cms_dashboard(self):
        """Administrator user successfully enters the CMS dashboard (HTTP 200)."""
        self.client.force_login(self.admin_user)
        response = self.client.get(self.cms_dash_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Content Management')


# ─────────────────────────────────────────────────────────────
# 6. CMS CRUD OPERATIONS (ADMIN WORKFLOW)
# ─────────────────────────────────────────────────────────────

class CMSCrudWorkflowTests(TestCase):
    """Verifies that admins can add, update, delete, and manage CMS resources."""

    def setUp(self):
        self.client = Client()
        self.admin = create_admin_user()
        self.client.force_login(self.admin)

    def test_admin_can_create_and_edit_banner(self):
        """Admin can create a new banner and subsequently update its title."""
        # Create
        create_url = reverse('cms:banner_create')
        payload = {
            'title': 'New Academic Year Drive',
            'subtitle': 'Enrollment campaign for primary grades',
            'button_text': 'Enroll Now',
            'button_link': '/programs/',
            'order': 2,
            'is_active': True,
        }
        response = self.client.post(create_url, payload)
        self.assertRedirects(response, reverse('cms:banner_list'))
        self.assertTrue(Banner.objects.filter(title='New Academic Year Drive').exists())

        # Edit
        banner = Banner.objects.get(title='New Academic Year Drive')
        edit_url = reverse('cms:banner_edit', kwargs={'pk': banner.pk})
        payload['title'] = 'Updated Academic Drive FY26'
        response = self.client.post(edit_url, payload)
        self.assertRedirects(response, reverse('cms:banner_list'))
        banner.refresh_from_db()
        self.assertEqual(banner.title, 'Updated Academic Drive FY26')

    def test_admin_can_delete_banner(self):
        """Admin can delete a banner via POST to the delete endpoint."""
        banner = Banner.objects.create(title='Temporary Banner to Delete', order=9)
        delete_url = reverse('cms:banner_delete', kwargs={'pk': banner.pk})
        response = self.client.post(delete_url)
        self.assertRedirects(response, reverse('cms:banner_list'))
        self.assertFalse(Banner.objects.filter(pk=banner.pk).exists())

    def test_admin_can_create_statistic(self):
        """Admin can add a new impact statistic."""
        create_url = reverse('cms:statistic_create')
        payload = {
            'label': 'Volunteers Mobilized',
            'value': '4,500+',
            'order': 3,
            'is_active': True,
        }
        response = self.client.post(create_url, payload)
        self.assertRedirects(response, reverse('cms:statistic_list'))
        self.assertTrue(Statistic.objects.filter(label='Volunteers Mobilized').exists())

    def test_admin_can_create_initiative(self):
        """Admin can register a new initiative."""
        create_url = reverse('cms:initiative_create')
        payload = {
            'title': 'Clean Water for Schools',
            'description': 'Water purification and sanitation stations for 50 schools.',
            'tag': 'Environment & Health',
            'link': '/programs/',
            'order': 4,
            'is_active': True,
        }
        response = self.client.post(create_url, payload)
        self.assertRedirects(response, reverse('cms:initiative_list'))
        self.assertTrue(Initiative.objects.filter(title='Clean Water for Schools').exists())

    def test_admin_can_toggle_inquiry_resolved_state(self):
        """Admin can toggle inquiry from unread/unresolved to resolved."""
        inquiry = ContactInquiry.objects.create(
            name='Sunita Rao',
            email='sunita@donor.org',
            message='Tax receipt inquiry',
            is_resolved=False,
        )
        toggle_url = reverse('cms:inquiry_toggle_resolved', kwargs={'pk': inquiry.pk})
        response = self.client.post(toggle_url)
        self.assertRedirects(response, reverse('cms:inquiry_list'))
        inquiry.refresh_from_db()
        self.assertTrue(inquiry.is_resolved)
