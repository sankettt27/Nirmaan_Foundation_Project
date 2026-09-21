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
" || true

echo "==> Build complete!"
