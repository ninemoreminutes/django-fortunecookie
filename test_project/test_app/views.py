# Django
from django.shortcuts import render_to_response
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView

# Django-FortuneCookie
from fortunecookie.models import FortuneCookie


def handle_error(request, status, title, message):
    template_name = 'error.html'
    if request.path.startswith('/admin/'):
        template_name = 'admin/%s' % template_name
    context = {
        'error_title': title,
        'error_message': message,
        'error_status': status,
    }
    response = render_to_response(template_name, context)
    response.status_code = status
    return response


def handle_400(request):
    title = _('Bad Request')
    message = _('The request could not be understood by the server.')
    return handle_error(request, 400, title, message)


def handle_403(request):
    title = _('Forbidden')
    message = _('You do not have permission to access the requested resource.')
    return handle_error(request, 403, title, message)


def handle_404(request):
    title = _('Not Found')
    message = _('The requested page could not be found.')
    return handle_error(request, 404, title, message)


def handle_500(request):
    title = _('Server Error')
    message = _('An internal server error has occurred.')
    return handle_error(request, 500, title, message)


class IndexView(DetailView):

    model = FortuneCookie
    template_name = 'test_app/index.html'

    def get_queryset(self):
        queryset = super(IndexView, self).get_queryset()
        return queryset.order_by('?')

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return queryset.first()


index = IndexView.as_view()
