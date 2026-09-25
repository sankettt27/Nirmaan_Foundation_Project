#!/usr/bin/env bash
# exit on error
set -o errexit

echo "==> Installing dependencies..."
pip install -r requirements.txt

echo "==> Collecting static files..."
python manage.py collectstatic --no-input

echo "==> Running database migrations..."
python manage.py migrate

echo "==> Ensuring default admin exists..."
python manage.py shell -c "
from accounts.models import CustomUser
if not CustomUser.objects.filter(role='admin').exists():
    CustomUser.objects.create_superuser(
        email='admin@nirmaan.org',
        full_name='Nirmaan Admin',
        password='Admin@123'
    )
    print('Default admin created: admin@nirmaan.org / Admin@123')
else:
    print('Admin user already exists.')
" || true

echo "==> Seeding default CMS content..."
python manage.py shell -c "
from cms.models import Banner, Statistic, Initiative, VisionMission

# Seed Banners
if not Banner.objects.exists():
    Banner.objects.create(
        title='One Mission.\nMany Ways to Create Change.',
        subtitle='Whether you are a passionate volunteer, a generous donor, or a committed corporate partner — Nirmaan Foundation is your platform to transform education and communities across India.',
        button_text='Become a Volunteer',
        button_link='#volunteer',
        order=1,
        is_active=True,
    )
    Banner.objects.create(
        title='Education is the\nMost Powerful Weapon',
        subtitle='Join thousands of volunteers teaching in underserved communities. Every weekend, every classroom, every child matters.',
        button_text='Start Volunteering',
        button_link='#volunteer',
        order=2,
        is_active=True,
    )
    print('Default banners created.')
else:
    print('Banners already exist.')

# Seed Statistics
if not Statistic.objects.exists():
    Statistic.objects.create(value='30K+', label='Children Impacted Every Year', icon='bi-people-fill', order=1)
    Statistic.objects.create(value='7.5K+', label='Active Volunteers Nationwide', icon='bi-heart-fill', order=2)
    Statistic.objects.create(value='18+', label='Cities Across India', icon='bi-geo-alt-fill', order=3)
    print('Default statistics created.')
else:
    print('Statistics already exist.')

# Seed Initiatives
if not Initiative.objects.exists():
    Initiative.objects.create(
        title='Strong Foundations',
        description='Weekend volunteer sessions in government schools and community centres that reinforce foundational literacy, numeracy, and life skills for children aged 6-14.',
        tag='In Schools',
        link='#programs',
        order=1,
    )
    Initiative.objects.create(
        title='Holistic Growth',
        description='After-school clubs for sports, arts, music, and socio-emotional learning that nurture the whole child — building confidence, creativity, and resilience beyond textbooks.',
        tag='Beyond Schools',
        link='#programs',
        order=2,
    )
    Initiative.objects.create(
        title='Future Changemakers',
        description='A flagship leadership track for young adults (18-25) that equips college students with social entrepreneurship, civic engagement, and community mobilisation skills.',
        tag='Youth Leadership',
        link='#programs',
        order=3,
    )
    print('Default initiatives created.')
else:
    print('Initiatives already exist.')

# Seed Vision / Mission
if not VisionMission.objects.exists():
    VisionMission.objects.create(
        section_type='vision',
        title='Our Vision',
        content='A future where every child in India has access to quality education, holistic development, and the opportunity to realise their full potential — regardless of their background.',
        icon='bi-eye-fill',
        order=1,
    )
    VisionMission.objects.create(
        section_type='mission',
        title='Our Mission',
        content='To empower communities through volunteer-driven education programmes, sustainable development initiatives, and partnerships that create lasting social impact across India.',
        icon='bi-bullseye',
        order=1,
    )
    print('Default vision/mission items created.')
else:
    print('Vision/Mission items already exist.')

# Seed New Sub-Page Models
from cms.models import (
    AboutMilestone, TeamMember, AboutEvent,
    ImpactStory, AnnualReport, VolunteerOpportunity,
    PartnerOrganization, OfficeLocation, FAQ
)

# 1. Milestones
if not AboutMilestone.objects.exists():
    AboutMilestone.objects.create(
        year='2014',
        title='Founding of Nirmaan Foundation',
        description='Started with 15 passionate college students conducting Sunday reading circles in two Bengaluru civic schools.',
        icon='bi-flag-fill',
        order=1
    )
    AboutMilestone.objects.create(
        year='2017',
        title='Ignite Program Expansion',
        description='Scaled foundational numeracy & literacy programs to 40 government schools across Karnataka and Maharashtra.',
        icon='bi-mortarboard-fill',
        order=2
    )
    AboutMilestone.objects.create(
        year='2020',
        title='Digital Learning & COVID Relief',
        description='Distributed 2,500+ refurbished tablets and provided digital tutoring kits to prevent dropouts during school closures.',
        icon='bi-laptop-fill',
        order=3
    )
    AboutMilestone.objects.create(
        year='2024',
        title='10-Year Decadal Milestone',
        description='Surpassed 30,000+ mentored students, 12,000+ active youth volunteers, and 150+ institutional school partnerships.',
        icon='bi-award-fill',
        order=4
    )
    print('Default milestones created.')

# 2. Team Members
if not TeamMember.objects.exists():
    TeamMember.objects.create(
        name='Dr. Ananya Sen',
        role='Co-Founder & Executive Director',
        category='leadership',
        bio='Former Teach For India Fellow and educator with 14+ years spearheading educational equity in public school networks.',
        order=1
    )
    TeamMember.objects.create(
        name='Vikramaditya Kulkarni',
        role='Head of Curriculum & Teacher Training',
        category='leadership',
        bio='Child cognitive psychologist specializing in bilingual foundational literacy and activity-based STEM learning.',
        order=2
    )
    TeamMember.objects.create(
        name='Pooja Deshmukh',
        role='Director of Volunteer Mobilization',
        category='leadership',
        bio='Has mobilized and mentored over 10,000 youth volunteers across 15 collegiate and corporate chapters in India.',
        order=3
    )
    TeamMember.objects.create(
        name='Prof. Ramesh Ramanathan',
        role='Senior Advisory Board Member',
        category='advisory',
        bio='Civic governance expert, urban policy scholar, and mentor to non-profit social innovations.',
        order=4
    )
    print('Default team members created.')

# 3. Events
if not AboutEvent.objects.exists():
    AboutEvent.objects.create(
        title='Annual National STEM & Robotics Mela 2025',
        event_date='Dec 14, 2025',
        location='Bengaluru, Karnataka',
        tag='STEM Exhibition',
        description='Over 1,200 students from 45 municipal schools exhibited hands-on science experiments, solar models, and robotic rovers.',
        order=1
    )
    AboutEvent.objects.create(
        title='Joy of Giving Volunteer Conclave',
        event_date='Oct 08, 2025',
        location='Pune, Maharashtra',
        tag='Volunteer Summit',
        description='500+ active educators and chapter coordinators gathered for pedagogy workshops, peer awards, and leadership training.',
        order=2
    )
    AboutEvent.objects.create(
        title='Project Disha Career Clinic & Scholarship Day',
        event_date='Jul 20, 2025',
        location='Hyderabad, Telangana',
        tag='Mentorship',
        description='One-on-one career counseling and higher education financial grants awarded to 180 adolescent girls from low-income households.',
        order=3
    )
    print('Default events created.')

# 4. Impact Stories
if not ImpactStory.objects.exists():
    ImpactStory.objects.create(
        name='Pooja Sharma',
        role_or_school='B.Tech Student & Disha Scholar',
        location='Bengaluru',
        quote='Before Nirmaan\'s math mentors came, I was terrified of exams. Today I am pursuing my dream in computer science.',
        story='Pooja attended weekend tutoring at a civic school in Bengaluru for 3 years. With dedicated mentors and fee support, she became the first college graduate in her family.',
        order=1
    )
    ImpactStory.objects.create(
        name='Ramesh Rao',
        role_or_school='Headmaster, Govt. High School',
        location='Pune',
        quote='Experiential science kits brought joy back into our classrooms. Attendance surged from 60% to 92%.',
        story='Under Headmaster Rao\'s leadership and Nirmaan\'s weekend volunteer teaching, the school recorded its highest board exam passing percentage in 15 years.',
        order=2
    )
    print('Default impact stories created.')

# 5. Annual Reports
if not AnnualReport.objects.exists():
    AnnualReport.objects.create(
        title='Annual Impact & Financial Disclosure Report',
        fiscal_year='FY 2024–25',
        summary='Audited balance sheets, school expansion assessments, and educational outcome indicators verified by independent evaluators.',
        order=1
    )
    AnnualReport.objects.create(
        title='Scaling Classroom Equity & Governance Audit',
        fiscal_year='FY 2023–24',
        summary='Detailed expenditure breakdown, 80G tax benefit compliance, and pedagogical evaluation of 150+ partner schools.',
        order=2
    )
    print('Default annual reports created.')

# 6. Volunteer Opportunities
if not VolunteerOpportunity.objects.exists():
    VolunteerOpportunity.objects.create(
        title='Weekend English & Foundational Numeracy Teacher',
        commitment='2 hrs/week (Sat/Sun)',
        mode='in_person',
        location='Bengaluru, Pune, Hyderabad, Delhi NCR',
        description='Deliver fun, activity-based lessons in English phonics and basic math for primary school children.',
        requirements='Conversational English, patience, empathy, and commitment to at least one 3-month academic semester.',
        order=1
    )
    VolunteerOpportunity.objects.create(
        title='Experiential STEM & Robotics Lab Guide',
        commitment='3 hrs/week (Weekend Mornings)',
        mode='hybrid',
        location='Bengaluru, Mumbai, Chennai',
        description='Lead middle school students through experiential science tinker kits, DIY experiments, and block coding.',
        requirements='Background in Engineering/BCA/B.Sc. Passion for practical, hands-on experiments.',
        order=2
    )
    VolunteerOpportunity.objects.create(
        title='Youth Career Mentor (Disha)',
        commitment='1 hr/week (Flexible)',
        mode='remote',
        location='Pan-India (Virtual 1-on-1)',
        description='Counsel Grade 11 & 12 youth on university admissions, entrance tests, vocational skills, and career clarity.',
        requirements='Working professional with 2+ years experience and strong listening skills.',
        order=3
    )
    print('Default volunteer opportunities created.')

# 7. Partners
if not PartnerOrganization.objects.exists():
    PartnerOrganization.objects.create(
        name='Tata Consultancy Services',
        category='corporate',
        testimonial='Nirmaan\'s ground-level rigor and transparent quarterly tracking made our STEM school sponsorship a remarkable success.',
        representative_name='CSR Lead, TCS',
        order=1
    )
    PartnerOrganization.objects.create(
        name='Infosys Foundation',
        category='foundation',
        testimonial='Their committed volunteer network ensures learning materials actually translate into measurable learning gains.',
        representative_name='Trustee, Infosys Foundation',
        order=2
    )
    print('Default partners created.')

# 8. Offices
if not OfficeLocation.objects.exists():
    OfficeLocation.objects.create(
        city='Bengaluru',
        address='#42, Shanti Nagar Main Road, Bengaluru, Karnataka 560027',
        email='bangalore@nirmaanfoundation.org',
        phone='+91 80 2222 3333',
        is_hq=True,
        order=1
    )
    OfficeLocation.objects.create(
        city='Pune Chapter',
        address='3rd Floor, Lotus Plaza, Karve Road, Kothrud, Pune, Maharashtra 411038',
        email='pune@nirmaanfoundation.org',
        phone='+91 20 2544 6789',
        is_hq=False,
        order=2
    )
    OfficeLocation.objects.create(
        city='Hyderabad Chapter',
        address='Plot 18, Road No. 2, Banjara Hills, Hyderabad, Telangana 500034',
        email='hyderabad@nirmaanfoundation.org',
        phone='+91 40 2333 4444',
        is_hq=False,
        order=3
    )
    print('Default offices created.')

# 9. FAQs
if not FAQ.objects.exists():
    FAQ.objects.create(
        category='volunteer',
        question='Do I need prior teaching experience to volunteer?',
        answer='Not at all! We provide a complete 14-day training induction covering lesson plans, classroom dynamics, and child safety. All you need is enthusiasm and empathy.',
        order=1
    )
    FAQ.objects.create(
        category='volunteer',
        question='What is the time commitment expected?',
        answer='Most volunteers teach for 2 hours on either Saturday or Sunday morning for one academic term (3 to 6 months).',
        order=2
    )
    FAQ.objects.create(
        category='partner',
        question='Are donations and CSR grants eligible for tax exemptions?',
        answer='Yes! Nirmaan Foundation is registered under Section 12A and Section 80G of the Income Tax Act, granting 50% tax exemption. We also possess an active MCA CSR-1 registration.',
        order=3
    )
    FAQ.objects.create(
        category='programs',
        question='How do you select the schools you work with?',
        answer='We partner directly with government, civic, and low-income affordable private schools that demonstrate high need and strong leadership enthusiasm for extracurricular support.',
    print('Default FAQs created.')

# 10. Assignment 3: Our Story, Core Values, Programs
from cms.models import OurStory, CoreValue, Program

if not OurStory.objects.exists():
    OurStory.objects.create(
        content=(
            "Founded in 2014 in Bengaluru, Nirmaan Foundation started as a grassroots initiative "
            "when 15 university students came together to address the urgent need for quality foundational "
            "education in underserved municipal schools. What began as weekend tutoring in two classrooms "
            "has grown into a nationwide community of educators, volunteers, and donors.\n\n"
            "Today, Nirmaan Foundation operates across 18+ cities with 7,500+ active youth volunteers, "
            "empowering over 30,000 children annually through structured literacy curricula, digital "
            "robotics labs, nutrition support, and youth mentorship. Our work is guided by the conviction "
            "that every child deserves the opportunity to realise their full potential."
        )
    )
    print('Default Our Story created.')

if not CoreValue.objects.exists():
    CoreValue.objects.create(value='Integrity', icon='bi-shield-check', order=1, description='Honesty, accountability, and the highest ethical standards in every project and resource entrusted to us.')
    CoreValue.objects.create(value='Inclusivity', icon='bi-people-fill', order=2, description='Ensuring equal learning and holistic growth opportunities for children irrespective of gender, religion, or background.')
    CoreValue.objects.create(value='Empathy', icon='bi-heart-fill', order=3, description='Deep listening, compassion, and understanding the grassroots challenges faced by underprivileged communities.')
    CoreValue.objects.create(value='Transparency', icon='bi-eye-fill', order=4, description='Open governance, audited disclosures, and complete visibility into our finances, operations, and impact metrics.')
    print('Default Core Values created.')

if not Program.objects.exists():
    Program.objects.create(name='Free Educational Resources', icon='bi-book-half', order=1, description='Providing free textbooks, digital tablets, experiential learning kits, and weekend literacy modules for children in government and low-income schools.')
    Program.objects.create(name='Health Camps for Rural Areas', icon='bi-hospital', order=2, description='Running pediatric check-ups, eye screenings, nutritional supplements, and hygiene workshops in underserved rural and peri-urban villages.')
    Program.objects.create(name='Vocational Training for Youth & Women', icon='bi-tools', order=3, description='Offering computer literacy, spoken English, and job-readiness skill workshops for youth and women to build sustainable livelihoods.')
    print('Default Programs created.')
" || true

echo "==> Build complete!"

