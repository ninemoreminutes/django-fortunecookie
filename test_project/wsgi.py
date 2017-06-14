# Python
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_project.settings')

# Django
from django.core.wsgi import get_wsgi_application  # noqa

application = get_wsgi_application()

# Whitenoise
try:
    from whitenoise.django import DjangoWhiteNoise  # noqa
    application = DjangoWhiteNoise(application)
except ImportError:
    pass
