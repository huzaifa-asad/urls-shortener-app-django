import os
import sys

# Add the project root (parent of api/) to Python path
# So 'urlshortener.settings' resolves to <root>/urlshortener/settings.py
ROOT = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urlshortener.settings')
os.environ.setdefault('VERCEL', '1')

# Use Django's standard WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()