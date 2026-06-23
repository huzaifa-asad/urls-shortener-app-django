import os
import sys

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urlshortener.settings')
os.environ.setdefault('VERCEL', '1')

# Create and configure the WSGI application directly
import django
from django.conf import settings
from django.core.wsgi import get_wsgi_application

# Run migrations on startup
django.setup()
from django.core.management import call_command
import sqlite3
try:
    # Try creating a writable database in /tmp
    db_path = '/tmp/db.sqlite3'
    conn = sqlite3.connect(db_path)
    conn.close()
    settings.DATABASES['default']['NAME'] = db_path
    call_command('migrate', '--noinput', verbosity=0)
except Exception:
    pass

application = get_wsgi_application()