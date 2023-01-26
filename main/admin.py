from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Celebrity, Client, Availability, OfferRequest, Payment, PaymentInformation


class ClientInline(admin.StackedInline):
    model = Client
    extra = 0


class CelebrityInline(admin.StackedInline):
    model = Celebrity
    extra = 0


class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (None,
         {
             "classes": ("wide",),
             "fields":  ("phone_number", "username", "password1", "password2"),
         }),
    )
    fieldsets = (
        ('Personal Info',
         {
             "fields": ("phone_number", "username", "password", "payment_details"),
         }),
        ('Misc Details', {
            "fields": ('first_name', 'last_name'),
        }),
        ('Admin Stuff', {
            'fields': ('is_staff', 'is_superuser', 'is_active', 'date_joined', 'groups', 'user_permissions')
        })
    )
    list_display = ("phone_number", "username", "email", "first_name", "last_name", "is_staff")
    ordering = ("phone_number", "username")
    inlines = [
        ClientInline,
        CelebrityInline,
    ]


admin.site.register(User, CustomUserAdmin)

admin.site.register(Client)
admin.site.register(Celebrity)
admin.site.register(Availability)

admin.site.register(Payment)
admin.site.register(PaymentInformation)
admin.site.register(OfferRequest)
