import os
import sys
from pathlib import Path


# Add the project root (parent of urlshortener/) to sys.path
# This way 'from urlshortener.wsgi' and 'urlshortener.settings' both work
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urlshortener.settings')
os.environ.setdefault('VERCEL', '1')

# Import the Django WSGI app from urlshortener package
from urlshortener.wsgi import application  # noqa: E402