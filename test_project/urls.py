# Django
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

urlpatterns = patterns('')

if 'django.contrib.admin' in settings.INSTALLED_APPS:
    from django.contrib import admin
    admin.autodiscover()
    #urlpatterns += patterns('',
    #    url(r'^$', RedirectView.as_view(url='/admin/')),
    #)
    urlpatterns += patterns('',
        url(r'^admin/', include(admin.site.urls)),
    )

if 'django.contrib.staticfiles' in settings.INSTALLED_APPS and settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
