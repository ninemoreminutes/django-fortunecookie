from test_project.settings import *

DEBUG = False

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(ROOT_PATH, 'fortune.sqlite3'),
    }
}

MEDIA_ROOT = os.path.join(ROOT_PATH, 'public', 'media')

STATIC_ROOT = os.path.join(ROOT_PATH, 'public', 'static')
