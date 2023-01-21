import logging
from typing import Any

from django.contrib.auth import get_user_model
from rest_framework import serializers

from . import models

UserModel = get_user_model()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class DiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Discussion
        fields = "__all__"
        depth = 1


class TextMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TextMessage
        fields = "__all__"
        depth = 1


class ImageMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ImageMessage
        fields = "__all__"
        depth = 1


class VoiceMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VoiceMessage
        fields = "__all__"
        depth = 1


class MessageInfoSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.filter())
    recepient = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.filter())
    textmessage = TextMessageSerializer(required=False)
    voicemessage = VoiceMessageSerializer(required=False)
    imagemessage = ImageMessageSerializer(required=False)
    discussion = DiscussionSerializer(required=False)

    class Meta:
        model = models.ChatMessageInfo
        fields = ['id', 'sender', 'recepient', 'date_sent', 'textmessage', 'voicemessage', 'imagemessage', 'discussion']
        depth = 2
