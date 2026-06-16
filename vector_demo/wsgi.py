"""WSGI config for the vector_demo project."""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vector_demo.settings")

application = get_wsgi_application()
