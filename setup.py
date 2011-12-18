#!/usr/bin/env python

# Python
import sys

# Setuptools
from setuptools import setup, find_packages

# Django-FortuneCookie
from fortunecookie import __VERSION__

# FIXME: This app needs my patched version of django-sortedm2m to work:
# git://github.com/ninemoreminutes/django-sortedm2m.git@d5a5e29820147e55d971ff6dc2cf73b1897c8ec1
try:
    import sortedm2m
    assert sortedm2m.__version__ == (0, 3, 3)
except (ImportError, AssertionError):
    print >> sys.stderr, 'django-sortedm2m==0.3.3 is required (install from github)'
    sys.exit(1)

setup(
    name='django-fortunecookie',
    version=__VERSION__,
    author='Nine More Minutes, Inc.',
    author_email='support@ninemoreminutes.com',
    description='Django models to store everything about fortune cookies.',
    long_description=file('README', 'rb').read(),
    license='BSD',
    keywords='django fortune cookie',
    url='https://projects.ninemoreminutes.com/projects/django-fortunecookie/',
    packages=find_packages(exclude=['test_project']),
    include_package_data=True,
    zip_safe=False,
    install_requires=['Django>=1.3', 'django-sortedm2m==0.3.3'],
    setup_requires=[],
    tests_require=['Django>=1.3', 'South>=0.7.3', 'django-sortedm2m==0.3.3', 'django-setuptest'],
    test_suite='test_project.TestSuite',
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
            'version': __VERSION__,
            'release': __VERSION__,
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
