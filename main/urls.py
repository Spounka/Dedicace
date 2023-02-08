from django.urls import path, include

from . import views

urlpatterns = [
    path(r"auth/", include("knox.urls")),

    # Client Endpoints
    path(r'client/', views.ClientCurrent.as_view(), name="client-current"),
    path(r'client/create/', views.ClientCreate.as_view(), name="client-create"),
    path(r'client/<int:pk>/', views.ClientReadUpdateDestroyAPIView.as_view(), name="client-rud"),
    path(r'client/offers/', views.RelatedOffersReadUpdate.as_view(), name="client-offers"),
    path(r'client/offers/<int:pk>/', views.RelatedOffersReadUpdate.as_view(), name="client-offers"),
    path(r'client/offers/<int:pk>/payment/', views.ViewOfferRequestPayment.as_view(), name="celeb-offer-payment"),
    path(r'client/payments/', views.PaymentAPIView.as_view(), name="client-payments"),
    path(r'client/payments/<int:pk>/', views.PaymentAPIView.as_view(), name="client-payment-id"),

    # Celebrity Endpoints
    path(r'celebs/', views.CelebrityList.as_view(), name="celeb-current"),
    path(r'celebs/from-phone/', views.GetCurrentCelebFromPhone.as_view(), name='celeb-from-phone'),
    path(r'celebs/current/', views.CelebrityCurrent.as_view(), name="celeb-current"),
    path(r'celebs/<int:pk>/', views.CelebrityReadUpdateAPIView.as_view(), name="celeb-ru"),
    path(r'celebs/offers/', views.RelatedOffersReadUpdate.as_view(), name="celeb-offers"),
    path(r'celebs/offers/<int:pk>/payment/', views.ViewOfferRequestPayment.as_view(), name="celeb-offer-payment"),

    # OfferRequest Endpoints
    path(r'reports/', views.ReportAPIView.as_view(), name="report"),

    # Availability Endpoints
    path(r'availabilities/', views.AvailabilityAPIView.as_view(), name="availabilities"),
]
