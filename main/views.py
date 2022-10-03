from knox.auth import TokenAuthentication
from rest_framework import viewsets, generics, mixins, response, status
from rest_framework.views import APIView

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


class FanAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FanSerializer
    queryset = Fan.objects.all()


class CreateFanAPIView(APIView, mixins.CreateModelMixin):
    def create(self, request, *args, **kwargs):
        serializer = FanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.get['phone_number'] = User.normalize_username(request.data['user']['phone_number'])
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request):
        if not request.data.get('user'):
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data={"reason": "user is empty"})
        user_serializer = UserSerializer(data=request.data['user'])
        if not user_serializer.is_valid(raise_exception=True):
            return response.Response(status=status.HTTP_400_BAD_REQUEST, data={"reason": "user issue"})
        user = user_serializer.save()

        serializer = FanSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data['user'] = user
            serializer.save()
            return response.Response(data={"status": "success"})
        return response.Response(data={"status": "failed"})


class GetCurrentUser(APIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        fan = Fan.objects.get(user=user)
        fan_serialiszer = FanSerializer(fan)
        return response.Response(data=fan_serialiszer.data, status=status.HTTP_200_OK)
