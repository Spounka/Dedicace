from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path(r"user/update/<int:pk>/", views.FanAPIView.as_view(), name="hello"),
    path(r"users/create/", views.CreateFanAPIView.as_view(), name="oss"),
    path(r"current/", views.GetCurrentUser.as_view(), name="logout"),
    path(r"auth/", include("knox.urls")),
]
