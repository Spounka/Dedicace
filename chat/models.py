from django.db import models
from django.conf import settings


# Create your models here.
class ChatMessageInfo(models.Model):
    date_sent = models.CharField(max_length=60, default="")
    sender: settings.AUTH_USER_MODEL = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sent_messages",
                                                         on_delete=models.SET_NULL, null=True)
    recepient: settings.AUTH_USER_MODEL = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="received_messages",
                                                            on_delete=models.SET_NULL, null=True)


class TextMessageInfo(models.Model):
    message_info = models.OneToOneField(ChatMessageInfo, on_delete=models.CASCADE)
    text_message = models.CharField(max_length=300, default="")


def get_media_chat_upload_path(instance: 'ImageMessageInfo', filename):
    return f"{instance.message_info.sender.username}/{instance.message_info.username}/" \
           f"{instance.message_info.date_sent}/{filename}"


class ImageMessageInfo(models.Model):
    message_info = models.OneToOneField(ChatMessageInfo, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_media_chat_upload_path)


class VoiceMessageInfo(ChatMessageInfo):
    message_info = models.OneToOneField(ChatMessageInfo, related_name="voidemessage", on_delete=models.CASCADE)
    audio = models.FileField(upload_to=get_media_chat_upload_path)
