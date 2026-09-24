"""
tests/test_assignment3.py — Comprehensive Test Suite for Assignment 3.

Covers:
  1. Database Design & Tables:
     - `our_story`: id, content, created_at, updated_at
     - `core_values`: id, value, created_at, updated_at
     - `programs`: id, name, description, created_at, updated_at
     - `team_members`: id, name, role, image_url, created_at, updated_at
  2. Access Control & Admin Protection for all About CMS views
  3. Our Story CRUD operations
  4. Core Values CRUD operations
  5. Programs CRUD operations
  6. Team Members CRUD operations
  7. Public About Us page (7 required frontend sections)
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db import connection

from cms.models import (
    OurStory, CoreValue, Program, TeamMember,
    AboutMilestone, AboutEvent, Statistic
)

User = get_user_model()


class Assignment3DatabaseDesignTest(TestCase):
    """
    Test suite verifying database design and table schema matching
    Assignment 3 Database Design document.
    """

    def test_our_story_table_name_and_fields(self):
        """Verify table `our_story` name, columns, and timestamp behavior."""
        self.assertEqual(OurStory._meta.db_table, 'our_story')

        story = OurStory.objects.create(
            content="Nirmaan Foundation was established in 2014 to ensure quality learning for every child."
        )
        self.assertIsNotNone(story.id)
        self.assertEqual(story.content, "Nirmaan Foundation was established in 2014 to ensure quality learning for every child.")
        self.assertIsNotNone(story.created_at)
        self.assertIsNotNone(story.updated_at)
        self.assertIn("Our Story", str(story))

    def test_core_values_table_name_and_fields(self):
        """Verify table `core_values` name, columns, and constraints."""
        self.assertEqual(CoreValue._meta.db_table, 'core_values')

        val = CoreValue.objects.create(
            value="Integrity",
            description="Honesty and transparency in every action.",
            icon="bi-shield-check",
            order=1,
            is_active=True
        )
        self.assertIsNotNone(val.id)
        self.assertEqual(val.value, "Integrity")
        self.assertIsNotNone(val.created_at)
        self.assertIsNotNone(val.updated_at)
        self.assertEqual(str(val), "Integrity")

    def test_programs_table_name_and_fields(self):
        """Verify table `programs` name, columns, and constraints."""
        self.assertEqual(Program._meta.db_table, 'programs')

        prog = Program.objects.create(
            name="Free Educational Resources",
            description="Providing learning materials, digital kits, and workbooks for government schools.",
            icon="bi-book-half",
            order=1,
            is_active=True
        )
        self.assertIsNotNone(prog.id)
        self.assertEqual(prog.name, "Free Educational Resources")
        self.assertIsNotNone(prog.created_at)
        self.assertIsNotNone(prog.updated_at)
        self.assertEqual(str(prog), "Free Educational Resources")

    def test_team_members_table_name_and_fields(self):
        """Verify table `team_members` name, columns, and image_url field."""
        self.assertEqual(TeamMember._meta.db_table, 'team_members')

        member = TeamMember.objects.create(
            name="Dr. Ananya Sen",
            role="Founder & Managing Trustee",
            category="leadership",
            bio="Pioneering education activist and grassroots pedagogue.",
            image_url="/static/images/team_founder.jpg",
            order=1,
            is_active=True
        )
        self.assertIsNotNone(member.id)
        self.assertEqual(member.name, "Dr. Ananya Sen")
        self.assertEqual(member.role, "Founder & Managing Trustee")
        self.assertEqual(member.image_url, "/static/images/team_founder.jpg")
        self.assertIsNotNone(member.created_at)
        self.assertIsNotNone(member.updated_at)
        self.assertIn("Dr. Ananya Sen", str(member))
        self.assertEqual(member.get_image_display_url(), "/static/images/team_founder.jpg")


class Assignment3AboutCMSBackendTest(TestCase):
    """
    Test suite verifying backend CMS control for Our Story, Core Values,
    Programs, and Team Members with role-based access control.
    """

    def setUp(self):
        self.client = Client()

        # Admin user
        self.admin_user = User.objects.create_user(
            email='admin@nirmaan.org',
            full_name='Admin Nirmaan',
            password='AdminPassword123!',
            role='admin',
            is_staff=True,
            is_superuser=True
        )

        # Volunteer (non-admin)
        self.volunteer_user = User.objects.create_user(
            email='volunteer@nirmaan.org',
            full_name='Volunteer User',
            password='VolunteerPassword123!',
            role='volunteer'
        )

    # ── Access Control Tests ──────────────────────────────────

    def test_about_cms_requires_admin_login(self):
        """Anonymous and non-admin users must be blocked from About CMS endpoints."""
        urls = [
            reverse('cms:about_cms_hub'),
            reverse('cms:our_story_edit'),
            reverse('cms:core_value_list'),
            reverse('cms:core_value_create'),
            reverse('cms:program_list'),
            reverse('cms:program_create'),
            reverse('cms:team_list'),
            reverse('cms:team_create'),
        ]
        for url in urls:
            # Anonymous -> redirect to login
            res_anon = self.client.get(url)
            self.assertEqual(res_anon.status_code, 302)

            # Non-admin -> forbidden or redirected
            self.client.force_login(self.volunteer_user)
            res_vol = self.client.get(url)
            self.assertIn(res_vol.status_code, [302, 403])
            self.client.logout()

    def test_about_cms_hub_view_loads_for_admin(self):
        """Admin can access the About CMS Hub and view metric cards."""
        self.client.force_login(self.admin_user)
        res = self.client.get(reverse('cms:about_cms_hub'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'cms/about_hub.html')
        self.assertContains(res, 'About Us Content Management')
        self.assertContains(res, 'Our Story')
        self.assertContains(res, 'Core Values')
        self.assertContains(res, 'Programs & Focus')
        self.assertContains(res, 'Team Members')

    # ── Our Story CMS Tests ───────────────────────────────────

    def test_our_story_create_and_edit_via_cms(self):
        """Admin can create and update Our Story content through CMS."""
        self.client.force_login(self.admin_user)

        # GET form
        res_get = self.client.get(reverse('cms:our_story_edit'))
        self.assertEqual(res_get.status_code, 200)

        # POST new story
        res_post = self.client.post(reverse('cms:our_story_edit'), {
            'content': 'Nirmaan Foundation was started in 2014 by 15 volunteers in Bengaluru.'
        })
        self.assertRedirects(res_post, reverse('cms:about_cms_hub'))

        story = OurStory.objects.first()
        self.assertIsNotNone(story)
        self.assertIn('started in 2014', story.content)

        # POST update existing story
        res_update = self.client.post(reverse('cms:our_story_edit'), {
            'content': 'Updated: Over 10 years, Nirmaan Foundation has empowered 30,000+ students.'
        })
        self.assertRedirects(res_update, reverse('cms:about_cms_hub'))
        story.refresh_from_db()
        self.assertIn('30,000+ students', story.content)

    # ── Core Values CMS CRUD Tests ────────────────────────────

    def test_core_values_full_crud_via_cms(self):
        """Admin can perform Create, Read, Update, Delete on Core Values."""
        self.client.force_login(self.admin_user)

        # 1. CREATE
        res_create = self.client.post(reverse('cms:core_value_create'), {
            'value': 'Empathy',
            'description': 'Listening deeply to community needs.',
            'icon': 'bi-heart-fill',
            'order': 1,
            'is_active': True,
        })
        self.assertRedirects(res_create, reverse('cms:core_value_list'))
        val = CoreValue.objects.get(value='Empathy')
        self.assertEqual(val.icon, 'bi-heart-fill')

        # 2. READ / LIST
        res_list = self.client.get(reverse('cms:core_value_list'))
        self.assertEqual(res_list.status_code, 200)
        self.assertContains(res_list, 'Empathy')

        # 3. UPDATE / EDIT
        res_edit = self.client.post(reverse('cms:core_value_edit', kwargs={'pk': val.pk}), {
            'value': 'Deep Empathy',
            'description': 'Listening deeply to community challenges and aspirations.',
            'icon': 'bi-heart-fill',
            'order': 2,
            'is_active': True,
        })
        self.assertRedirects(res_edit, reverse('cms:core_value_list'))
        val.refresh_from_db()
        self.assertEqual(val.value, 'Deep Empathy')
        self.assertEqual(val.order, 2)

        # 4. DELETE
        res_del = self.client.post(reverse('cms:core_value_delete', kwargs={'pk': val.pk}))
        self.assertRedirects(res_del, reverse('cms:core_value_list'))
        self.assertFalse(CoreValue.objects.filter(pk=val.pk).exists())

    # ── Programs CMS CRUD Tests ───────────────────────────────

    def test_programs_full_crud_via_cms(self):
        """Admin can perform Create, Read, Update, Delete on Programs."""
        self.client.force_login(self.admin_user)

        # 1. CREATE
        res_create = self.client.post(reverse('cms:program_create'), {
            'name': 'Rural Health Camps',
            'description': 'Providing free pediatric screenings and nutritional packs.',
            'icon': 'bi-hospital',
            'order': 1,
            'is_active': True,
        })
        self.assertRedirects(res_create, reverse('cms:program_list'))
        prog = Program.objects.get(name='Rural Health Camps')

        # 2. READ / LIST
        res_list = self.client.get(reverse('cms:program_list'))
        self.assertEqual(res_list.status_code, 200)
        self.assertContains(res_list, 'Rural Health Camps')

        # 3. UPDATE / EDIT
        res_edit = self.client.post(reverse('cms:program_edit', kwargs={'pk': prog.pk}), {
            'name': 'Comprehensive Rural Health Camps',
            'description': 'Screenings, dental care, and vitamins for rural children.',
            'icon': 'bi-hospital-fill',
            'order': 1,
            'is_active': True,
        })
        self.assertRedirects(res_edit, reverse('cms:program_list'))
        prog.refresh_from_db()
        self.assertEqual(prog.name, 'Comprehensive Rural Health Camps')

        # 4. DELETE
        res_del = self.client.post(reverse('cms:program_delete', kwargs={'pk': prog.pk}))
        self.assertRedirects(res_del, reverse('cms:program_list'))
        self.assertFalse(Program.objects.filter(pk=prog.pk).exists())

    # ── Team Members CMS CRUD Tests ───────────────────────────

    def test_team_members_full_crud_via_cms(self):
        """Admin can manage Team Members in `team_members` table."""
        self.client.force_login(self.admin_user)

        # 1. CREATE
        res_create = self.client.post(reverse('cms:team_create'), {
            'name': 'Suresh Reddy',
            'role': 'Director of Volunteer Operations',
            'category': 'leadership',
            'bio': 'Manages 7,500+ volunteer leaders across chapters.',
            'image_url': '/static/images/team_suresh.jpg',
            'order': 1,
            'is_active': True,
        })
        self.assertRedirects(res_create, reverse('cms:team_list'))
        member = TeamMember.objects.get(name='Suresh Reddy')
        self.assertEqual(member.role, 'Director of Volunteer Operations')
        self.assertEqual(member.image_url, '/static/images/team_suresh.jpg')

        # 2. LIST
        res_list = self.client.get(reverse('cms:team_list'))
        self.assertEqual(res_list.status_code, 200)
        self.assertContains(res_list, 'Suresh Reddy')

        # 3. EDIT
        res_edit = self.client.post(reverse('cms:team_edit', kwargs={'pk': member.pk}), {
            'name': 'Suresh Reddy, MBA',
            'role': 'Chief Operating Officer & Volunteer Lead',
            'category': 'leadership',
            'bio': 'Expanded volunteer networks across 18 cities.',
            'image_url': '/static/images/team_suresh.jpg',
            'order': 1,
            'is_active': True,
        })
        self.assertRedirects(res_edit, reverse('cms:team_list'))
        member.refresh_from_db()
        self.assertEqual(member.name, 'Suresh Reddy, MBA')

        # 4. DELETE
        res_del = self.client.post(reverse('cms:team_delete', kwargs={'pk': member.pk}))
        self.assertRedirects(res_del, reverse('cms:team_list'))
        self.assertFalse(TeamMember.objects.filter(pk=member.pk).exists())


class Assignment3AboutUsFrontendViewTest(TestCase):
    """
    Test suite verifying public About Us page frontend matches all
    7 sections from Assignment 3 Introduction & Frontend guidelines.
    """

    def setUp(self):
        self.client = Client()

        # Seed test data for all sections
        self.story = OurStory.objects.create(
            content="Founded in 2014, Nirmaan Foundation started as a small grassroots initiative."
        )

        self.val1 = CoreValue.objects.create(value="Integrity", icon="bi-shield-check", order=1)
        self.val2 = CoreValue.objects.create(value="Inclusivity", icon="bi-people-fill", order=2)
        self.val3 = CoreValue.objects.create(value="Empathy", icon="bi-heart-fill", order=3)
        self.val4 = CoreValue.objects.create(value="Transparency", icon="bi-eye-fill", order=4)

        self.prog1 = Program.objects.create(
            name="Free Educational Resources",
            description="Providing free textbooks, digital tablets, and literacy kits.",
            order=1
        )
        self.prog2 = Program.objects.create(
            name="Health Camps for Rural Areas",
            description="Comprehensive pediatric check-ups and nutrition packs.",
            order=2
        )

        self.member1 = TeamMember.objects.create(
            name="Anand Kumar",
            role="Executive Director",
            category="leadership",
            bio="Over 12 years in development sector leadership.",
            order=1
        )

        self.stat1 = Statistic.objects.create(label="Children Empowered", value="30K+", order=1)
        self.event1 = AboutEvent.objects.create(title="Annual Foundational Literacy Festival", order=1)

    def test_public_about_us_page_renders_all_7_sections(self):
        """Verify public /about/ page renders all 7 required sections with dynamic data."""
        res = self.client.get(reverse('home:about'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/about.html')

        # Section 1: Introduction Section
        self.assertContains(res, 'id="introduction"')
        self.assertContains(res, 'About Nirmaan Foundation')
        self.assertContains(res, 'Welcome to Nirmaan Foundation!')

        # Section 2: History and Background (Our Story)
        self.assertContains(res, 'id="our-story"')
        self.assertContains(res, 'Founded in 2014, Nirmaan Foundation started as a small grassroots initiative.')

        # Section 3: Core Values
        self.assertContains(res, 'id="core-values"')
        self.assertContains(res, 'Integrity')
        self.assertContains(res, 'Inclusivity')
        self.assertContains(res, 'Empathy')
        self.assertContains(res, 'Transparency')

        # Section 4: Areas of Focus / Programs
        self.assertContains(res, 'id="programs"')
        self.assertContains(res, 'Free Educational Resources')
        self.assertContains(res, 'Health Camps for Rural Areas')

        # Section 5: Leadership and Team
        self.assertContains(res, 'id="team"')
        self.assertContains(res, 'Anand Kumar')
        self.assertContains(res, 'Executive Director')

        # Section 6: Impact and Achievements
        self.assertContains(res, 'id="impact"')
        self.assertContains(res, '30K+')
        self.assertContains(res, 'Annual Foundational Literacy Festival')

        # Section 7: Call to Action (CTA)
        self.assertContains(res, 'id="cta"')
        self.assertContains(res, 'Volunteer Today')
        self.assertContains(res, 'Support / Donate')
