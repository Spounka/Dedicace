import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.handlers.wsgi import WSGIRequest
from knox.auth import TokenAuthentication
from rest_framework import generics, response, status
from rest_framework.permissions import IsAuthenticated

from . import models, serializers

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

UserModel = get_user_model()


# Create your views here.
class DiscussionAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.DiscussionSerializer
    queryset = models.Discussion.objects.all

    def get(self, request, *args, **kwargs):
        if (pk := kwargs.get('pk')) is not None:
            try:
                discussion = models.Discussion.objects.get(pk=pk)
                messages = discussion.chatmessageinfo_set.all()
                result = serializers.MessageInfoSerializer(messages, many=True)
                logger.info(f'found discussion with id {discussion.pk}')
                return response.Response(status=status.HTTP_200_OK, data=result.data)
            except models.Discussion.DoesNotExist:
                logger.error(f'discussion with pk {pk} does not exist')
                return response.Response(status=status.HTTP_404_NOT_FOUND)
        return super().get(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        user: settings.AUTH_USER_MODEL = request.user
        discussions = models.Discussion.objects.filter(members__pk=user.pk)
        data = serializers.DiscussionSerializer(discussions, many=True)
        return response.Response(status=status.HTTP_200_OK, data=data.data)


class MessageInfoAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.MessageInfoSerializer
    queryset = models.ChatMessageInfo.objects.get

    def create(self, request: WSGIRequest, *args, **kwargs):
        request.data['sender'] = request.user.pk
        return super().create(request, *args, **kwargs)
