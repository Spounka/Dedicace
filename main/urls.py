from django.urls import path, include
from . import views

urlpatterns = [
    path(r"auth/", include("knox.urls")),
    path(r'client/'),
]
