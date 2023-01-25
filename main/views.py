from django.contrib.auth import user_logged_in, login
from django.contrib.auth.hashers import make_password
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from knox.settings import knox_settings
from rest_framework import generics, mixins, response, status
from rest_framework.fields import DateTimeField
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer

from .models import User, Celebrity, Client, OfferRequest, Payment, Report
from .serializers import (
    UserSerializer, CelebritySerializer, ClientSerializer, OfferRequestSerializer,
    PaymentSerializer, AvailabilitySerializer, ReportSerializer
)


class ViewCurrentModel(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)
    model = None

    def retrieve(self, request, *args, **kwargs):
        obj = self.model.objects.filter(user_id=request.user.id).first()
        if obj:
            return response.Response(self.serializer_class(obj).data, status.HTTP_200_OK)
        return response.Response(status.HTTP_403_FORBIDDEN)


def get_expiry_datetime_format():
    return knox_settings.EXPIRY_DATETIME_FORMAT


def format_expiry_datetime(expiry):
    datetime_format = get_expiry_datetime_format()
    return DateTimeField(format=datetime_format).to_representation(expiry)


def get_ttl():
    return knox_settings.TOKEN_TTL


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = ClientSerializer
    model = None

    def create(self, request, *args, **kwargs):
        serializer: ModelSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client: Client = serializer.save()
        user = client.user
        ttl = get_ttl()
        login(request, user, backend='main.auth.UserAuthUsernameIsPhone')
        instance, token = AuthToken.objects.create(user, ttl)
        user_logged_in.send(sender=request.user.__class__,
                            request=request, user=request.user)
        data = {
            'expiry': format_expiry_datetime(instance.expiry),
            'token':  token
        }

        return response.Response(data=data, status=status.HTTP_201_CREATED)


class WithUserSupportAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)
    model = None

    def update(self, request, *args, **kwargs):
        if not self.is_editing_self(request, args, kwargs):
            return response.Response(status=status.HTTP_403_FORBIDDEN)

        # makes sure we don't accidentally change user's id
        request.data.pop('id', None)

        user_data: dict[str, str] = request.data.pop('user', None)
        user: User = self.get_object().user
        if user_data:
            # if we changed the password, we have to hash it, so we don't store it raw
            if user_data.get('password', None):
                user_data['password'] = make_password(user_data['password'])
            if user_data.get('phone_number', None):
                user_data['phone_number'] = User.normalize_username(user_data['phone_number'])

            # remove fields that may cause vulnerabilities
            user_data.pop('id', None)
            user_data.pop('is_superuser', None)
            user_data.pop('is_staff', None)
            user_data.pop('is_active', None)
            user_data.pop('groups', None)
            user_data.pop('user_permissions', None)

            user_serializer = UserSerializer(instance=user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
        return super().update(request, args, kwargs)

    def delete(self, request, *args, **kwargs):
        if not self.is_editing_self(request, args, kwargs):
            return response.Response(status=status.HTTP_403_FORBIDDEN)
        request.user.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        if not self.is_editing_self(request, args, kwargs) and not request.user.is_celebrity():
            return response.Response(status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, args, kwargs)

    def is_editing_self(self, request, *args, **kwargs) -> bool:
        obj = self.model.objects.filter(user_id=request.user.pk).first()
        if not obj:
            return False
        return True


class ClientCurrent(ViewCurrentModel):
    serializer_class = ClientSerializer
    model = Client


class ClientCreate(UserCreateAPIView):
    serializer_class = ClientSerializer
    model = Client


class ClientReadUpdateDestroyAPIView(WithUserSupportAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.filter()
    model = Client


class CelebrityCurrent(ViewCurrentModel):
    serializer_class = CelebritySerializer
    model = Celebrity


class CelebrityList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)
    serializer_class = CelebritySerializer
    queryset = Celebrity.objects.all()


class CelebrityCreate(UserCreateAPIView):
    serializer_class = CelebritySerializer
    model = Celebrity

    def create(self, request, *args, **kwargs):
        self.args_to_add['price'] = request.data.get('price', '00')
        self.args_to_add['is_available'] = request.data.get('is_available', True)
        self.args_to_add['availability'] = request.data.get('availability', None)
        return super().create(request, args, kwargs)


class CelebrityReadUpdateAPIView(WithUserSupportAPIView):
    serializer_class = CelebritySerializer
    queryset = Celebrity.objects.filter()
    model = Celebrity


class RelatedOffersReadUpdate(generics.ListCreateAPIView, mixins.RetrieveModelMixin):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)
    serializer_class = OfferRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer: OfferRequestSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['sender'] = request.user
        celebrity = Celebrity.objects.filter(pk=request.data.get('recepient')).first()
        if not celebrity:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)
        serializer.validated_data['recepient'] = celebrity.user
        serializer.save()
        return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk', None):
            if OfferRequest.objects.get(pk=kwargs['pk']).sender != request.user:
                return response.Response(status=status.HTTP_403_FORBIDDEN)
            return super().retrieve(request, args, kwargs)
        return super().get(request, args, kwargs)

    def list(self, request, *args, **kwargs):
        if request.user.is_client():
            offers = OfferRequest.objects.filter(sender=request.user)
            serializer = OfferRequestSerializer(offers, many=True)
            return response.Response(data=serializer.data, status=status.HTTP_200_OK)
        elif request.user.is_celebrity():
            offers = OfferRequest.objects.filter(recepient=request.user)
            serializer = OfferRequestSerializer(offers, many=True)
            return response.Response(data=serializer.data, status=status.HTTP_200_OK)
        return response.Response(status=status.HTTP_403_FORBIDDEN)


class PaymentAPIView(generics.ListCreateAPIView, mixins.RetrieveModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.filter()
    serializer_class = PaymentSerializer

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk', None):
            if Payment.objects.get(pk=kwargs['pk']).offerrequest.sender != request.user:
                return response.Response(status=status.HTTP_403_FORBIDDEN)
            return super().retrieve(request, args, kwargs)
        return super().get(request, args, kwargs)

    def list(self, request, *args, **kwargs):
        if request.user.is_client():
            offers = Payment.objects.filter(offerrequest__sender=request.user)
            payment_serializer = PaymentSerializer(offers, many=True)
            return response.Response(data=payment_serializer.data, status=status.HTTP_200_OK)
        elif request.user.is_celebrity():
            offers = Payment.objects.filter(offerrequest__recepient=request.user)
            payment_serializer = PaymentSerializer(offers, many=True)
            return response.Response(data=payment_serializer.data, status=status.HTTP_200_OK)
        return response.Response(status=status.HTTP_403_FORBIDDEN)


class ViewOfferRequestPayment(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)
    serializer_class = PaymentSerializer
    queryset = Payment.objects.filter()

    def get(self, request, *args, **kwargs):
        offer = OfferRequest.objects.filter(pk=kwargs['pk']).first()
        if not offer:
            return response.Response(status=status.HTTP_404_NOT_FOUND)
        if offer.recepient != request.user:
            return response.Response(status=status.HTTP_403_FORBIDDEN)
        if not hasattr(offer, "payment"):
            return response.Response(data={"message": "Offer has no payment yet"}, status=status.HTTP_400_BAD_REQUEST)
        payment_serializer = PaymentSerializer(offer.payment)
        return response.Response(data=payment_serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        offer = OfferRequest.objects.filter(pk=kwargs.get('pk')).first()
        if request.user != offer.sender or request.user != offer.recepient:
            return response.Response(status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, args, kwargs)


class ReportAPIView(generics.ListCreateAPIView, mixins.RetrieveModelMixin):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)
    serializer_class = ReportSerializer
    queryset = Report.objects.filter()
    parser_classes = (MultiPartParser,)

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk', None):
            return self.retrieve(request, args, kwargs)
        return super().get(request, args, kwargs)

    def list(self, request, *args, **kwargs):
        if not request.user.is_celebrity():
            return response.Response(status=status.HTTP_403_FORBIDDEN)
        reports = Report.objects.filter(reporter=request.user)
        serializer = ReportSerializer(reports, many=True)
        return response.Response(status=status.HTTP_200_OK, data=serializer.data)

    def post(self, request, *args, **kwargs):
        if not request.user.is_celebrity():
            return response.Response(status=status.HTTP_403_FORBIDDEN)
        reported = Client.objects.filter(pk=request.data.get('reported')).first()
        if not reported:
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "User not found"})
        report_serializer = ReportSerializer(data=request.data)
        report_serializer.is_valid(raise_exception=True)
        report_serializer.validated_data['reporter'] = request.user
        report_serializer.validated_data['reported'] = reported.user
        report_serializer.save()
        return response.Response(status=status.HTTP_201_CREATED, data=report_serializer.data)


class AvailabilityAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)
    serializer_class = AvailabilitySerializer

    def get(self, request, *args, **kwargs):
        if not request.user.is_celebrity():
            return response.Response(status=status.HTTP_403_FORBIDDEN)
        return super().get(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.is_celebrity():
            return response.Response(status=status.HTTP_403_FORBIDDEN)
        return super().post(request, args, kwargs)
