import os
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent / 'urlshortener'
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urlshortener.settings')

from urlshortener.wsgi import application  # noqa: E402
