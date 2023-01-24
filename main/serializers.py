from rest_framework import serializers

from .models import User, Celebrity, Client, OfferRequest, Payment, Report


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "phone_number", "username", "payment_details"]


class GenereicUserModelsSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict[str, Any]):
        user_data = validated_data.pop('user')
        password: str = user_data.pop('password')
        user_data['phone_number'] = User.normalize_username(user_data['phone_number'])
        user: User = User.objects.create(**user_data)
        user.set_password(password)
        client = Client.objects.create(user=user, **validated_data)
        return client


class ClientSerializer(GenereicUserModelsSerializer):
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


class CelebritySerializer(GenereicUserModelsSerializer):
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
