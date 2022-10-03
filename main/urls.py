from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"users", views.UserViewSet, basename="user")
router.register(r"celebrities", views.CelebrityViewSet, basename="celebs")
router.register(r"fans", views.FanViewSet, basename="fans")
router.register(r"requests", views.RequestViewSet, basename="requests")
router.register(r"payments", views.PaymentViewSet, basename="payments")

urlpatterns = [
    path(r"user/update/<int:pk>/", views.FanAPIView.as_view(), name="hello"),
    path(r"users/create/", views.CreateFanAPIView.as_view(), name="oss"),
    path(r"current/", views.GetCurrentUser.as_view(), name="logout"),
    path(r"auth/", include("knox.urls")),
    path('', include(router.urls)),
]
