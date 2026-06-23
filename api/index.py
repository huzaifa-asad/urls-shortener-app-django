import os
import sys
from pathlib import Path


# Add the urlshortener directory to path so 'urlshortener.settings' can be found
PROJECT_ROOT = Path(__file__).resolve().parent.parent / 'urlshortener'
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Also add parent so manage.py can be found
PARENT_ROOT = Path(__file__).resolve().parent.parent
if str(PARENT_ROOT) not in sys.path:
    sys.path.insert(0, str(PARENT_ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urlshortener.settings')
os.environ.setdefault('VERCEL', '1')

# Run migrations on cold start to ensure tables exist
import django
django.setup()
from django.core.management import call_command
try:
    call_command('migrate', '--noinput', verbosity=0)
except Exception:
    pass  # Tables already exist

# Import the Django WSGI app
from wsgi import application  # noqa: E402
