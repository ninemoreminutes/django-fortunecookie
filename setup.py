#!/usr/bin/env python

# Python
import sys

# Setuptools
from setuptools import setup, find_packages

# Django-FortuneCookie
from fortunecookie import __version__

tests_require=[
    'Django',
    #'django-debug-toolbar',
    'django-devserver',
    'django-extensions',
    'django-sortedm2m',
    'django-setuptest',
    'South',
],

try:
    import argparse
except ImportError:
    tests_require.append('argparse')

setup(
    name='django-fortunecookie',
    version=__version__,
    author='Nine More Minutes, Inc.',
    author_email='support@ninemoreminutes.com',
    description='Django models to store everything about fortune cookies.',
    long_description=file('README', 'rb').read(),
    license='BSD',
    keywords='django fortune cookie',
    url='https://projects.ninemoreminutes.com/projects/django-fortunecookie/',
    packages=['fortunecookie'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django>=1.3',
        'django-sortedm2m>=0.4.0',
    ],
    tests_require=tests_require,
    setup_requires=[],
    test_suite='test_suite.TestSuite',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
    ],
    options={
        'egg_info': {
            'tag_svn_revision': 1,
            'tag_build': '.dev',
        },
        'build_sphinx': {
            'source_dir': 'docs',
            'build_dir': 'docs/_build',
            'all_files': True,
            'version': __version__,
            'release': __version__,
        },
        'upload_sphinx': {
            'upload_dir': 'docs/_build/html',
        },
        'aliases': {
            # FIXME: Add 'test' to both aliases below.
            'dev_build': 'egg_info sdist build_sphinx',
            'release_build': 'egg_info -b "" -R sdist build_sphinx',
        },
    },
)
