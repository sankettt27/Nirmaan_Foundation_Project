"""
config/test_settings.py — Test-only settings override.

Uses SQLite in-memory database so the test suite can run
without a MySQL server running locally.

Usage:
    python manage.py test tests.test_assignment1 --settings=config.test_settings

The production database configuration (MySQL) is unchanged in settings.py.
This override is ONLY for running automated tests without a MySQL connection.
"""

from .settings import *  # noqa: F401, F403 — intentional wildcard import

# Override the database to use SQLite for tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
