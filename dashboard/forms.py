from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from dashboard.validators import empty_validator, alphabetic_validator, validate_phone_number
from main import models


class AdminLoginForm(forms.Form):
    authenticator = forms.CharField(
        label=_("Username or Phone number"),
        widget=forms.TextInput(attrs={"placeholder": _("Phone number")}),
        error_messages={'invalid': _("Invalide Kho")}
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": _("Password")}),
        error_messages={'invalid': _("Invalide Kho")}
    )


class CreateCelebForm(forms.Form):
    phone_number = forms.CharField(
        label=_("Phone Number"),
        max_length=20,
        widget=forms.TextInput(attrs={"placeholder": _("Phone Number")}),
        validators=[validate_phone_number, empty_validator]
    )
    name = forms.CharField(
        label=_("Name"),
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": _("Name")}),
        validators=[alphabetic_validator]
    )
    last_name = forms.CharField(
        label=_("Last Name"),
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": _("Last Name")}),
        validators=[alphabetic_validator]
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={"placeholder": _("Email")}),
    )
    username = forms.CharField(
        label=_("Username"),
        widget=forms.TextInput(attrs={"placeholder": _("Username")}),
    )
    ccp = forms.CharField(
        label=_("CCP"),
        widget=forms.TextInput(attrs={"placeholder": _("CCP")}),
        required=False,
        empty_value=None
    )
    rip = forms.CharField(
        label=_("RIP"),
        widget=forms.TextInput(attrs={"placeholder": _("RIP")}),
        required=False,
        empty_value=None
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": _("Address"), "rows": 5})
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        user = models.User.objects.filter(phone_number=phone_number).first()
        if user:
            raise ValidationError(
                _("Phone Number already exists"),
                code='1'
            )
        return phone_number

    def clean_email(self):
        email = self.cleaned_data['email']
        if models.User.objects.filter(email=email).first():
            raise ValidationError(
                _("Email already exists"),
                code='2'
            )
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if models.User.objects.filter(username=username).first():
            raise ValidationError(
                _("Username already exists"),
                code='3'
            )
        return username

    def clean_ccp(self):
        ccp = self.cleaned_data['ccp']
        if ccp is not None and models.PaymentInformation.objects.filter(ccp=ccp).first():
            raise ValidationError(
                _("CCP already exists"),
                code='4'
            )
        return ccp

    def clean_rip(self):
        rip = self.cleaned_data['rip']
        if rip is not None and models.PaymentInformation.objects.filter(rip=rip).first():
            raise ValidationError(
                _("RIP already exists"),
                code='5'
            )
        return rip
