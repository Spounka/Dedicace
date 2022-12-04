from rest_framework import serializers
from .models import User, Celebrity, Client, OfferRequest, Payment, Report


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"
        depth = 1


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        depth = 1


class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        depth = 2


class CelebritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Celebrity
        fields = "__all__"
        depth = 1


class OfferRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferRequest
        fields = "__all__"
        depth = 1


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"
        depth = 2
