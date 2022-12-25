from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import reverse
from . import forms
from main import models


# Create your views here.
class CreateCelebrityAPIView(LoginRequiredMixin, generic.FormView):
    template_name = 'dashboard/views/create_celeb.html'
    login_url = reverse_lazy('dashboard-login')
    form_class = forms.CreateCelebForm

    def get_success_url(self):
        return reverse('dashboard-create-celeb')

    def get_context_data(self, **kwargs):
        kwargs['celeb_active'] = 'celeb-active'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        payment_details = models.PaymentInformation(
            ccp=form.cleaned_data['ccp'] or None,
            rip=form.cleaned_data['rip'] or None,
            address=form.cleaned_data['address']
        )
        payment_details.save()

        user = models.User(
            username=form.cleaned_data['username'],
            phone_number=form.cleaned_data['name'],
            email=form.cleaned_data['email'],
            first_name=form.cleaned_data['name'],
            last_name=form.cleaned_data['last_name'],
            payment_details=payment_details
        )
        user.save()

        celeb = models.Celebrity(user=user, description="", price=0, is_available=True)
        celeb.save()
        return super().form_valid(form)


class AdminLogin(generic.FormView):
    form_class = forms.AdminLoginForm
    template_name = 'dashboard/views/admin_login.html'
    success_url = reverse_lazy('dashboard-create-celeb')
    request = None

    def post(self, request, *args, **kwargs):
        self.request = request
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        authenticator = form.cleaned_data['authenticator']
        password = form.cleaned_data['password']
        user = authenticate(self.request, phone_number=authenticator, password=password)
        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(self.get_success_url())
        return self.form_invalid(form)
