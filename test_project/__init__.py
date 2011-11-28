# Python
import os

# django-setuptest
import setuptest

class TestSuite(setuptest.SetupTestSuite):

    def __init__(self, *args, **kwargs):
        os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'
        from south.management.commands import patch_for_test_db_setup
        patch_for_test_db_setup()
        super(TestSuite, self).__init__(*args, **kwargs)
