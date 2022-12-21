from django.core.handlers.wsgi import WSGIRequest
from django.views import generic
from . import forms


# Create your views here.
class CreateCelebrityAPIView(generic.FormView):
    template_name = 'dashboard/views/create_celeb.html'
    form_class = forms.CreateCelebForm

    def get_context_data(self, **kwargs):
        kwargs['celeb_active'] = 'celeb-active'
        return super().get_context_data(**kwargs)

    def post(self, request: WSGIRequest, *args, **kwargs):
        return super().post(request, args, kwargs)
