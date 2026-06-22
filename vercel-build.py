#!/usr/bin/env python
import os
import sys

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urlshortener.settings')

# Add paths so 'urlshortener' package can be found
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_dir)
sys.path.insert(0, os.path.join(base_dir, 'urlshortener'))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()