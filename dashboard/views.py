import mimetypes
import os

from django.conf import settings
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import AccessMixin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from main import models
from . import forms

User = get_user_model()


# Create your views here.
def is_admin_or_staff(user_obj: User):
    if not user_obj.is_authenticated:
        return False
    return user_obj.is_staff or user_obj.is_superuser


def index(request):
    if is_admin_or_staff(request.user):
        return HttpResponseRedirect(reverse('dashboard-create-celeb'))
    return HttpResponseRedirect(reverse('dashboard-login'))


class IsAdminOrStaffMixin(AccessMixin):
    permission_denied_message = _("You do not have permission to view this")

    def dispatch(self, request, *args, **kwargs):
        if not is_admin_or_staff(request.user):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class CreateCelebrityAPIView(IsAdminOrStaffMixin, generic.FormView):
    template_name = 'dashboard/views/create_celeb.html'
    login_url = reverse_lazy('dashboard-login')
    form_class = forms.CreateCelebForm
    success_url = reverse_lazy('dashboard-create-celeb')

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
    request = None

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('dashboard-create-celeb'))
        return super().get(request, *args, **kwargs)

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


class PaymentsView(IsAdminOrStaffMixin, generic.ListView):
    template_name = 'dashboard/views/payments.html'
    model = models.Payment
    paginate_by = 5
    request: WSGIRequest = None
    login_url = reverse_lazy('dashboard-login')
    success_url = reverse_lazy('dashboard-view-payments')

    def get(self, request, *args, **kwargs):
        self.request = request
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        status_filter = self.request.GET.get('filter', None)
        search_filter = self.request.GET.get('search', None)
        object_list = self.model.objects.all()
        if status_filter:
            object_list = object_list.filter(payment_status=status_filter)
        else:
            object_list = object_list.exclude(payment_status="updated")
        if search_filter:
            object_list = object_list.filter(
                Q(offerrequest__sender__username__icontains=search_filter) |
                Q(offerrequest__recepient__username__icontains=search_filter) |
                Q(offerrequest__sender__first_name__icontains=search_filter) |
                Q(offerrequest__sender__last_name__icontains=search_filter) |
                Q(offerrequest__recepient__first_name__icontains=search_filter) |
                Q(offerrequest__recepient__last_name__icontains=search_filter)
            )
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs['payment_active'] = 'payment-active'
        kwargs['search_value'] = self.request.GET.get('search', '')

        kwargs['all_payments'] = self.model.objects.all().count()
        kwargs['confirmed_payments'] = self.model.objects.filter(payment_status='confirmed').count()
        kwargs['pending_payments'] = self.model.objects.filter(payment_status='pending').count()
        kwargs['refused_payments'] = self.model.objects.filter(payment_status='refused').count()
        kwargs['updated_payments'] = self.model.objects.filter(payment_status='updated').count()

        return super().get_context_data(object_list=object_list, **kwargs)


class UsersView(IsAdminOrStaffMixin, generic.ListView):
    login_url = reverse_lazy('dashboard-login')
    ...


def download_file(request):
    if request.method == "POST":
        file_path = request.POST.get('file-path')
        download_path = os.path.join(settings.MEDIA_ROOT, file_path)
        if os.path.exists(download_path):
            with open(download_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_path)[0])
                response['Content-Disposition'] = f'attachment; filename={os.path.basename(download_path)}'
                response['Content-Length'] = len(response.content)
                return response
        raise Http404
    return HttpResponseForbidden()
