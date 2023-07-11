from __future__ import annotations

import logging
from typing import Any

from django.contrib.auth import get_user_model
from rest_framework import serializers

from . import models

UserModel = get_user_model()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TextMessageSerializer(serializers.ModelSerializer):
    message_info = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.TextMessage
        fields = "__all__"
        depth = 1


class ImageMessageSerializer(serializers.ModelSerializer):
    message_info = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.ImageMessage
        fields = "__all__"
        depth = 1


class VoiceMessageSerializer(serializers.ModelSerializer):
    message_info = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.VoiceMessage
        fields = "__all__"
        depth = 1


class MessageInfoDiscussionView(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(read_only=True)
    recepient = serializers.PrimaryKeyRelatedField(read_only=True)
    textmessage = TextMessageSerializer()
    voicemessage = VoiceMessageSerializer()
    imagemessage = ImageMessageSerializer()

    class Meta:
        model = models.ChatMessageInfo
        fields = ['id', 'sender', 'recepient', 'date_sent', 'textmessage', 'voicemessage', 'imagemessage']
        depth = 0


class DiscussionSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    messages = MessageInfoDiscussionView(many=True)

    class Meta:
        model = models.Discussion
        fields = ['id', 'members', 'messages']
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
        depth = 1

    def create(self, validated_data: dict[str, Any]):
        sender = UserModel.objects.get(pk=validated_data.get('sender').pk)
        recepient = UserModel.objects.get(pk=validated_data.get('recepient').pk)
        logger.info(f'details: {sender=} {recepient=}')
        discussion = models.Discussion.objects \
            .filter(members__exact=sender.pk) \
            .filter(members__exact=recepient.pk).first()
        if not discussion:
            logger.error(f'no discussion found for users with pk {sender.pk} and {recepient.pk}')
            discussion = models.Discussion.objects.create()
            discussion.members.add(sender)
            discussion.members.add(recepient)
        if (textmessage := validated_data.pop('textmessage', None)) is not None:
            message_info = models.ChatMessageInfo.objects.create(discussion=discussion, **validated_data)
            models.TextMessage.objects.create(message_info=message_info, **textmessage)
        elif (imagemessage := validated_data.pop('imagemessage', None)) is not None:
            message_info = models.ChatMessageInfo.objects.create(discussion=discussion, **validated_data)
            models.ImageMessage.objects.create(message_info=message_info, **imagemessage)
        elif (voicemessage := validated_data.pop('voicemessage', None)) is not None:
            message_info = models.ChatMessageInfo.objects.create(discussion=discussion, **validated_data)
            models.VoiceMessage.objects.create(message_info=message_info, **voicemessage)
        else:
            raise serializers.ValidationError('Need to pass voice_message or text_message or image_message')
        return message_info
