# Python
import os
import sys

# Django
from django.conf import global_settings

# Update this module's local settings from the global settings module.
this_module = sys.modules[__name__]
for setting in dir(global_settings):
    if setting == setting.upper():
        setattr(this_module, setting, getattr(global_settings, setting))

# Absolute path to the directory containing this Django project.
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'test_project.sqlite3'),
    }
}

SITE_ID = 1

SECRET_KEY = '1a93a98e-03e7-4787-b099-0209705b80aa'

STATIC_URL = '/static/'

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

ROOT_URLCONF = 'test_project.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'debug_toolbar',
    'devserver',
    'django_extensions',
    'south',
    'sortedm2m',
    'fortunecookie',
)

INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

DEVSERVER_DEFAULT_ADDR = '127.0.0.1'
DEVSERVER_DEFAULT_PORT = '8066'

DEVSERVER_MODULES = (
    #'devserver.modules.sql.SQLRealTimeModule',
    'devserver.modules.sql.SQLSummaryModule',
    'devserver.modules.profile.ProfileSummaryModule',
    # Modules not enabled by default
    #'devserver.modules.ajax.AjaxDumpModule',
    #'devserver.modules.profile.MemoryUseModule',
    #'devserver.modules.cache.CacheSummaryModule',
    #'devserver.modules.profile.LineProfilerModule',
)

TEST_RUNNER = 'hotrunner.HotRunner'

EXCLUDED_TEST_APPS = [x for x in INSTALLED_APPS if x != 'fortunecookie']
