#!/usr/bin/env python
import os
import sys

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urlshortener.settings')

# Add the urlshortener directory to path so 'urlshortener.settings' can be found
project_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'urlshortener')
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

# Also add the parent directory
parent_dir = os.path.dirname(os.path.abspath(__file__))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()