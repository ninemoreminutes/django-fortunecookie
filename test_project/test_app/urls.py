# Django
from django.conf.urls import url

# Test App
from test_project.test_app.views import index


app_name = 'test_app'

urlpatterns = [
    url(r'^$', index, name='index'),
]
