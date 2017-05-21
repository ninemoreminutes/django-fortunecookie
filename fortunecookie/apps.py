# Django
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class FortuneCookieConfig(AppConfig):

    name = 'fortunecookie'
    verbose_name = _('Fortune cookies')
