"""
cms/management/commands/seed_assignment3.py — Seeds default data for Assignment 3.

Populates tables:
  - our_story
  - core_values
  - programs
  - team_members (if empty)
"""

from django.core.management.base import BaseCommand
from cms.models import OurStory, CoreValue, Program, TeamMember


class Command(BaseCommand):
    help = 'Seeds initial content for Assignment 3 (Our Story, Core Values, Programs, Team Members)'

    def handle(self, *args, **options):
        # 1. Seed Our Story
        story, created = OurStory.objects.get_or_create(
            id=1,
            defaults={
                'content': (
                    "Founded in 2014 in Bengaluru, Nirmaan Foundation started as a grassroots initiative "
                    "when 15 university students came together to address the urgent need for quality foundational "
                    "education in underserved municipal schools. What began as weekend tutoring in two classrooms "
                    "has grown into a nationwide community of educators, volunteers, and donors.\n\n"
                    "Today, Nirmaan Foundation operates across 18+ cities with 7,500+ active youth volunteers, "
                    "empowering over 30,000 children annually through structured literacy curricula, digital "
                    "robotics labs, nutrition support, and youth mentorship. Our work is guided by the conviction "
                    "that every child deserves the opportunity to realise their full potential."
                )
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('[OK] Seeded Our Story content'))
        else:
            self.stdout.write('  Our Story already exists')

        # 2. Seed Core Values
        values_data = [
            {
                'value': 'Integrity',
                'icon': 'bi-shield-check',
                'order': 1,
                'description': 'Honesty, accountability, and the highest ethical standards in every project and resource entrusted to us.',
            },
            {
                'value': 'Inclusivity',
                'icon': 'bi-people-fill',
                'order': 2,
                'description': 'Ensuring equal learning and holistic growth opportunities for children irrespective of gender, religion, or background.',
            },
            {
                'value': 'Empathy',
                'icon': 'bi-heart-fill',
                'order': 3,
                'description': 'Deep listening, compassion, and understanding the grassroots challenges faced by underprivileged communities.',
            },
            {
                'value': 'Transparency',
                'icon': 'bi-eye-fill',
                'order': 4,
                'description': 'Open governance, audited disclosures, and complete visibility into our finances, operations, and impact metrics.',
            },
        ]
        for v in values_data:
            obj, c = CoreValue.objects.get_or_create(
                value=v['value'],
                defaults={
                    'icon': v['icon'],
                    'order': v['order'],
                    'description': v['description'],
                    'is_active': True,
                }
            )
            if c:
                self.stdout.write(self.style.SUCCESS(f"[OK] Seeded Core Value: {v['value']}"))

        # 3. Seed Programs
        programs_data = [
            {
                'name': 'Free Educational Resources',
                'icon': 'bi-book-half',
                'order': 1,
                'description': 'Providing free textbooks, digital tablets, experiential learning kits, and weekend literacy modules for children in government and low-income schools.',
            },
            {
                'name': 'Health Camps for Rural Areas',
                'icon': 'bi-hospital',
                'order': 2,
                'description': 'Running pediatric check-ups, eye screenings, nutritional supplements, and hygiene workshops in underserved rural and peri-urban villages.',
            },
            {
                'name': 'Vocational Training for Youth & Women',
                'icon': 'bi-tools',
                'order': 3,
                'description': 'Offering computer literacy, spoken English, and job-readiness skill workshops for youth and women to build sustainable livelihoods.',
            },
        ]
        for p in programs_data:
            obj, c = Program.objects.get_or_create(
                name=p['name'],
                defaults={
                    'icon': p['icon'],
                    'order': p['order'],
                    'description': p['description'],
                    'is_active': True,
                }
            )
            if c:
                self.stdout.write(self.style.SUCCESS(f"[OK] Seeded Program: {p['name']}"))

        # 4. Seed Team Members if empty
        if not TeamMember.objects.exists():
            team_data = [
                {
                    'name': 'Anand Kumar',
                    'role': 'Co-Founder & Executive Director',
                    'category': 'leadership',
                    'bio': '12+ years in development sector and grassroots education policy. Alumnus of TISS Mumbai.',
                    'order': 1,
                },
                {
                    'name': 'Dr. Priya Iyer',
                    'role': 'Head of Curriculum & Pedagogy',
                    'category': 'leadership',
                    'bio': 'Child psychologist and education specialist designing experiential literacy modules.',
                    'order': 2,
                },
                {
                    'name': 'Vikramaditya Rao',
                    'role': 'Strategic Advisor & CSR Lead',
                    'category': 'advisory',
                    'bio': 'Senior advisor bridging institutional CSR investments with grassroots community programs.',
                    'order': 3,
                },
            ]
            for m in team_data:
                TeamMember.objects.create(**m)
                self.stdout.write(self.style.SUCCESS(f"[OK] Seeded Team Member: {m['name']}"))

        self.stdout.write(self.style.SUCCESS('\nAssignment 3 database seeding complete!'))
