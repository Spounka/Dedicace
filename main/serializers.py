from __future__ import annotations

from typing import Any

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User, Celebrity, Client, OfferRequest, Payment, Report, PaymentInformation


class PaymentInformationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = PaymentInformation


class UserSerializer(serializers.ModelSerializer):
    payment_details = PaymentInformationSerializer(required=False)

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "phone_number", "username", "payment_details", 'password']


class ReturnUserSerializer(serializers.ModelSerializer):
    payment_details = PaymentInformationSerializer(required=False)

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "phone_number", "username", "payment_details"]


class GenereicUserModelsSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    def create(self, validated_data: dict[str, Any]):
        user_data = validated_data.pop('user')
        password: str = user_data.pop('password')
        user_data['phone_number'] = User.normalize_username(user_data['phone_number'])
        payment_information = None
        if user_data.get('payment_details', None):
            payment_data = user_data.pop('payment_details')
            payment_information = PaymentInformation.objects.create(**payment_data)
        user: User = User.objects.create(payment_details=payment_information, **user_data)
        user.set_password(password)
        user.save()
        client = Client.objects.create(user=user, **validated_data)
        return client

    def update(self, instance: Client | Celebrity, validated_data: dict[str, Any]):
        user_data = validated_data.pop('user', None)
        if not user_data:
            raise ValidationError('No user found')
        user = instance.user
        user.username = user_data.get('username', user.username)
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.email = user_data.get('email', user.email)
        if (password := user_data.get('password', None)) is not None:
            user.set_password(password)
        user.save()
        instance.wilaya = validated_data.get('wilaya', instance.wilaya)
        instance.save()
        return instance


class ClientSerializer(GenereicUserModelsSerializer):
    class Meta:
        model = Client
        fields = ['id', 'user', 'wilaya']
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


class CelebritySerializer(GenereicUserModelsSerializer):
    class Meta:
        model = Celebrity
        fields = "__all__"
        depth = 1


class CreationOfferRequestSerializer(serializers.ModelSerializer):
    recepient = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter())

    class Meta:
        model = OfferRequest
        exclude = ['sender']
        depth = 1

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        offer_request = OfferRequest.objects.create(**validated_data)
        payment = Payment.objects.create()
        payment.save()
        offer_request.payment = payment
        offer_request.save()
        return offer_request


class OfferRequestSerializer(serializers.ModelSerializer):
    sender = ReturnUserSerializer()
    recepient = ReturnUserSerializer()

    class Meta:
        model = OfferRequest
        fields = "__all__"
        depth = 1


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"
        depth = 2
