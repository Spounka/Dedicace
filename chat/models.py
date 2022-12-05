from django.db import models
from django.conf import settings


# Create your models here.
class ChatMessage(models.Model):
    date_sent = models.CharField(max_length=60, default="")
    sender: settings.AUTH_USER_MODEL = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    recepient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True


class TextMessage(ChatMessage):
    text_message = models.CharField(max_length=300, default="")


def get_media_chat_upload_path(instance: 'ImageMessage', filename):
    return f"{instance.sender.username}/{instance.recepient.username}/{instance.date_sent}/{filename}"


class ImageMessage(ChatMessage):
    image = models.ImageField(upload_to=get_media_chat_upload_path)


class VoiceMessage(ChatMessage):
    audio = models.FileField(upload_to=get_media_chat_upload_path)
