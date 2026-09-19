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

echo "==> Build complete!"
