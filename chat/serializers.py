from rest_framework import serializers
from . import models


class MessageInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChatMessageInfo
        fields = "__all__"


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
