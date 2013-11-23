# Python
from optparse import make_option

# Django
from django.core.management.base import BaseCommand, CommandError
from django.core import serializers
from django.utils import simplejson


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--indent', default=None, dest='indent', type='int',
                    help='Specifies the indent level to use when '
                    'pretty-printing output'),
        make_option('-n', '--natural', action='store_true',
                    dest='use_natural_keys', default=True, help='Use natural '
                    'keys if they are available.'),
        make_option('--pks', action='store_true', dest='use_primary_keys',
                    default=False, help='Use integer primary keys instead of '
                    'natural keys'),
    )
    help = ('Perform a simple dump of fortune cookie models to generate '
            'the fortunecookies test fixture (JSON only for now).')
    args = ''

    def handle(self, **options):
        from django.db.models import get_app, get_apps, get_models, get_model
        indent = options.get('indent', None)
        show_traceback = options.get('traceback', False)
        use_natural_keys = options.get('use_natural_keys', True)
        if options.get('use_primary_keys', False):
            use_natural_keys = False

        app_label = 'fortunecookie'
        try:
            app = get_app(app_label)
        except ImproperlyConfigured:
            raise CommandError("Unknown application: %s" % app_label)

        # Now collate the objects to be serialized.
        objects = []
        for model in get_models(app):
            objects.extend(model._default_manager.all())
        try:
            jsondata = serializers.serialize('json', objects, indent=indent,
                                             use_natural_keys=use_natural_keys)
            serialized_objects = simplejson.loads(jsondata)
            for obj in serialized_objects:
                if 'fields' in obj:
                    # Replace Django 1.4 created/modified timestamps with a
                    # format compatible with Django 1.3.
                    for field in ('created', 'modified'):
                        if field in obj['fields']:
                            value = obj['fields'][field]
                            value = value.replace('T', ' ')
                            value = value[:value.find('.')]
                            obj['fields'][field] = value
            return simplejson.dumps(serialized_objects, indent=indent)
        except Exception, e:
            if show_traceback:
                raise
            raise CommandError("Unable to serialize fortune cookies: %s" % e)
