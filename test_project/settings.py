# Python
import os
import sys

# Django
import django
from django.conf import global_settings

# DJ Database URL
try:
    import dj_database_url
except ImportError:
    dj_database_url = None

# Update this module's local settings from the global settings module.
this_module = sys.modules[__name__]
for setting in dir(global_settings):
    if setting == setting.upper():
        setattr(this_module, setting, getattr(global_settings, setting))

# Absolute path to the directory containing this Django project.
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'test_project.sqlite3'),
    }
}

if dj_database_url:
    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES['default'].update(db_from_env)

SITE_ID = 1

SECRET_KEY = '1a93a98e-03e7-4787-b099-0209705b80aa'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'public', 'static')

STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static'),
]

try:
    import whitenoise  # noqa
    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
except ImportError:
    pass

if django.VERSION >= (1, 10):
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
else:
    MIDDLEWARE_CLASSES = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            os.path.join(PROJECT_ROOT, 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ROOT_URLCONF = 'test_project.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django_extensions',
    'sortedm2m',
    'fortunecookie',
    'test_project.test_app',
)

WSGI_APPLICATION = 'test_project.wsgi.application'

INTERNAL_IPS = ('127.0.0.1',)

try:
    import debug_toolbar  # noqa
    INSTALLED_APPS += ('debug_toolbar',)
    if django.VERSION >= (1, 10):
        MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    else:
        MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }
except ImportError:
    pass

RUNSERVER_DEFAULT_ADDR = '127.0.0.1'
RUNSERVER_DEFAULT_PORT = '8066'
