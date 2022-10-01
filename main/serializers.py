from rest_framework import serializers
from .models import User, Celebrity, Fan, Request, Payment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class CelebritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Celebrity
        fields = "__all__"
        depth = 1


class FanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fan
        fields = "__all__"
        depth = 1


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = "__all__"
        depth = 1


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        depth = 1
