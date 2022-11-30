from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Celebrity, Client, Availability, OfferRequest, Payment


class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (None,
         {
             "classes": ("wide",),
             "fields":  ("phone_number", "username", "password1", "password2"),
         }),
    )
    list_display = ("phone_number", "username", "email", "first_name", "last_name", "is_staff")
    ordering = ("phone_number", "username")


admin.site.register(User, CustomUserAdmin)

admin.site.register(Client)
admin.site.register(Celebrity)
admin.site.register(Availability)

admin.site.register(Payment)
admin.site.register(OfferRequest)
