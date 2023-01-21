from rest_framework import serializers

from main.serializers import UserSerializer
from . import models


class DiscussionSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True)

    class Meta:
        model = models.Discussion
        fields = "__all__"
        depth = 2


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
