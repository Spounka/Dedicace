from knox.auth import TokenAuthentication
from rest_framework import generics, mixins, response, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import BasicAuthentication
from rest_framework.parsers import FormParser, MultiPartParser

from .models import User, Celebrity, Client, OfferRequest, Payment, models
from .serializers import (
    UserSerializer, CelebritySerializer, FanSerializer,
    RequestSerializer, PaymentSerializer,
)


class CelebrityAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CelebritySerializer
    queryset = Celebrity.objects.all()


class FanAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FanSerializer
    queryset = Client.objects.all()


class FanDestroyAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = FanSerializer
    queryset = Client.objects.all()


class CreateFanAPIView(APIView, mixins.CreateModelMixin):
    def post(self, request):
        if not request.data.get('user'):
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "user is empty"})
        user_serializer = UserSerializer(data=request.data['user'])
        if not user_serializer.is_valid(raise_exception=True):
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "user invalid"})
        user = user_serializer.save()
        user.phone_number = User.normalize_username(user.phone_number)
        user.save()

        serializer = FanSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data['user'] = user
            serializer.save()
            return response.Response(data={"message": "success"})
        return response.Response(data={"message": "failed"}, status=status.HTTP_400_BAD_REQUEST)


class GetCurrentUser(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = User.objects.filter(pk=request.user.id)[0]
        if not user:
            return response.Response(data={"message": "user not found"}, status=status.HTTP_400_BAD_REQUEST)
        fan = Client.objects.filter(user=user)
        if fan[0]:
            fan_serialiszer = FanSerializer(fan[0])
            return response.Response(data={**fan_serialiszer.data}, status=status.HTTP_200_OK)
        celebrity = Celebrity.objects.filter(user=user)
        if celebrity[0]:
            celeb_serialiszer = CelebritySerializer(celebrity[0])
            return response.Response(data=celeb_serialiszer.data, status=status.HTTP_200_OK)
        user_serializer = UserSerializer(user)
        return response.Response(data=user_serializer.data, status=status.HTTP_200_OK)


class RequestsAPIView(generics.GenericAPIView, mixins.ListModelMixin):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, BasicAuthentication)

    def list(self, request, *args, **kwargs):
        user = User.objects.filter(pk=request.user.pk).all()
        if user[0].request_sender:
            serializer = RequestSerializer(user[0].request_sender.all(), many=True)
        else:
            serializer = RequestSerializer(user[0].request_recipient.all(), many=True)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        return self.list(request)


class RequestCreateAPIView(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request_serializer = RequestSerializer(data=request.data)
        if not request_serializer.is_valid():
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data=request_serializer.errors)
        request_serializer.validated_data['sender'] = request.user
        recepient = User.objects.filter(pk=request.data.get('recepient')).first()
        request_serializer.validated_data['recepient'] = recepient
        payment_serializer = PaymentSerializer(data=request.data.get('payment'))
        if not payment_serializer.is_valid:
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data=payment_serializer.errors)
        # payment_serializer.is_valid(raise_exception=True)
        # payment_serializer.validated_data['receipt'] = request.data.get('receipt')
        # payment_serializer.save()
        # request_serializer.validated_data['payment'] = payment_serializer.data
        request_serializer.save()
        return response.Response(status=status.HTTP_200_OK, data=request_serializer.data)
