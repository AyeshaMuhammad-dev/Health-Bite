"""
Pytest configuration and fixtures.
"""
import pytest
import os
import django
from django.conf import settings

# Configure Django settings for tests
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_core.settings')

# Setup Django
django.setup()


@pytest.fixture(scope='session')
def django_db_setup():
    """Setup Django database for tests."""
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
