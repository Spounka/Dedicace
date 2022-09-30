from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Celebrity, Fan, Disponibility, Request, Payment


class CustomUserAdmin(UserAdmin):
    list_display = ("phone_number", "username", "email", "first_name", "last_name", "is_staff")
    ordering = ("phone_number", "username")


admin.site.register(User, CustomUserAdmin)

admin.site.register(Fan)
admin.site.register(Celebrity)
admin.site.register(Disponibility)

admin.site.register(Payment)
admin.site.register(Request)
