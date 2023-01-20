from knox.auth import TokenAuthentication
from rest_framework import generics, response, status, parsers
from rest_framework.permissions import IsAuthenticated

from main import models as m
from . import models, serializers


# Create your views here.
class DiscussionAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.MessageInfoSerializer

    def list(self, request, *args, **kwargs):
        try:
            user = m.Client.objects.get(pk=kwargs.get('pk')).user
        except m.Client.DoesNotExist:
            user = m.Celebrity.objects.get(pk=kwargs.get('pk')).user
        messages = models.ChatMessageInfo.objects.filter(
            models.Q(sender=user) | models.Q(recepient=user))
        return response.Response(data=serializers.TextMessageSerializer(messages, many=True).data,
                                 status=status.HTTP_200_OK)


class TextMessageAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.TextMessageSerializer

    def list(self, request, *args, **kwargs):
        if request.user.is_celebrity():
            recepient = m.Client.objects.get(pk=kwargs.get('pk')).user
            messages = models.TextMessage.objects.filter(message_info__sender=request.user,
                                                         message_info__recepient=recepient)
        elif request.user.is_client():
            sender = m.Celebrity.objects.get(pk=kwargs.get('pk')).user
            messages = models.TextMessage.objects.filter(message_info__recepient=request.user,
                                                         message_info__sender=sender)
        else:
            return response.Response(status=status.HTTP_403_FORBIDDEN)
        return response.Response(data=serializers.TextMessageSerializer(messages, many=True).data,
                                 status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        if not request.user.is_celebrity():
            return response.Response(status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.TextMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recepient = m.Client.objects.filter(pk=kwargs.get('pk')).first()
        if not recepient:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)
        message_info = models.ChatMessageInfo(
            sender=request.user, recepient=recepient.user)
        message_info.date_sent = request.data['date_sent']
        message_info.save()
        serializer.validated_data['message_info'] = message_info
        serializer.save()
        return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)


class ImageMessageAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ImageMessageSerializer
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)

    def list(self, request, *args, **kwargs):
        if request.user.is_celebrity():
            messages = models.ImageMessage.objects.filter(
                message_info__sender=request.user)
        elif request.user.is_client():
            messages = models.ImageMessage.objects.filter(
                message_info__recepient=request.user)
        else:
            return response.Response(status=status.HTTP_403_FORBIDDEN)
        return response.Response(data=serializers.ImageMessageSerializer(messages, many=True).data,
                                 status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        if not request.user.is_celebrity():
            return response.Response(status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.ImageMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recepient = m.Client.objects.filter(pk=kwargs.get('pk')).first()
        if not recepient:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)
        message_info = models.ChatMessageInfo(
            sender=request.user, recepient=recepient.user)
        message_info.date_sent = request.data['date_sent']
        message_info.save()
        serializer.validated_data['message_info'] = message_info
        serializer.save()
        return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)


class VoiceMessageAPIView(generics.ListCreateAPIView):
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.VoiceMessageSerializer

    def list(self, request, *args, **kwargs):
        if request.user.is_celebrity():
            messages = models.VoiceMessage.objects.filter(
                message_info__sender=request.user)
        elif request.user.is_client():
            messages = models.VoiceMessage.objects.filter(
                message_info__recepient=request.user)
        else:
            return response.Response(status=status.HTTP_403_FORBIDDEN)
        return response.Response(data=serializers.VoiceMessageSerializer(messages, many=True).data,
                                 status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        if not request.user.is_celebrity():
            return response.Response(status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.VoiceMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recepient = m.Client.objects.filter(pk=kwargs.get('pk')).first()
        if not recepient:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)
        message_info = models.ChatMessageInfo(
            sender=request.user, recepient=recepient.user)
        message_info.date_sent = request.data['date_sent']
        message_info.save()
        serializer.validated_data['message_info'] = message_info
        serializer.save()
        return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
