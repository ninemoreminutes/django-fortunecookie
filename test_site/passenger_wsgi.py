#!/usr/bin/env python
"""Activate virtualenv and run management command (or run as WSGI app)."""

# Python
import os
import sys

INTERP = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'env', 'bin', 'python')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Activate the virtualenv.
VIRTUALENV_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'env')
activate_this = os.path.join(VIRTUALENV_ROOT, 'bin', 'activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

# Add source dirctory to path
import fortunecookie  # noqa
SRC_PATH = os.path.abspath(os.path.dirname(fortunecookie.__file__))
sys.path.insert(0, SRC_PATH)
sys.path.insert(1, os.path.abspath(os.path.dirname(__file__)))

os.environ['DJANGO_SETTINGS_MODULE'] = 'site_settings'

# Django
from django.core.management import execute_from_command_line  # noqa
from django.core.wsgi import get_wsgi_application  # noqa

application = get_wsgi_application()
from paste.exceptions.errormiddleware import ErrorMiddleware  # noqa
application = ErrorMiddleware(application, debug=True)

if __name__ == '__main__':
    execute_from_command_line(sys.argv)
