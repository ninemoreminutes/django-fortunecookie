# Django
from django.conf import settings
from django.conf.urls import include, url
from django.utils.module_loading import import_string

# Test App
import test_project.test_app.urls

handler400 = 'test_project.test_app.views.handle_400'
handler403 = 'test_project.test_app.views.handle_403'
handler404 = 'test_project.test_app.views.handle_404'
handler500 = 'test_project.test_app.views.handle_500'

urlpatterns = [
    url(r'', include(test_project.test_app.urls)),
]

if 'debug_toolbar' in settings.INSTALLED_APPS and settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

if 'django.contrib.admin' in settings.INSTALLED_APPS:
    from django.contrib import admin
    admin.autodiscover()
    urlpatterns += [
        url(r'^admin/', include(admin.site.urls)),
    ]

if 'django.contrib.staticfiles' in settings.INSTALLED_APPS and settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += [
        url(r'^(?:admin/)?400.html$', import_string(handler400)),
        url(r'^(?:admin/)?403.html$', import_string(handler403)),
        url(r'^(?:admin/)?404.html$', import_string(handler404)),
        url(r'^(?:admin/)?500.html$', import_string(handler500)),
    ]
