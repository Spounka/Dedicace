from django.shortcuts import render
from rest_framework import viewsets
from .models import User, Celebrity, Fan, Request, Payment
from .serializers import UserSerializer, CelebritySerializer, FanSerializer, RequestSerializer, PaymentSerializer


# Create your views here.
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CelebrityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Celebrity.objects.all()
    serializer_class = CelebritySerializer


class FanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Fan.objects.all()
    serializer_class = FanSerializer


class RequestViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
