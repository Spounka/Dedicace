from rest_framework import serializers
from .models import User, Celebrity, Fan, Request, Payment, Report


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class FanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fan
        fields = "__all__"
        depth = 1


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        depth = 1


class DisponibilitySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        depth = 2


class CelebritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Celebrity
        fields = "__all__"
        depth = 1


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = "__all__"
        depth = 1


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"
        depth = 2
