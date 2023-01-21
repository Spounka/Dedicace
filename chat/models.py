from django.conf import settings
from django.db import models


# Create your models here.
class Discussion(models.Model):
    parties = models.ManyToManyField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class ChatMessageInfo(models.Model):
    sender: settings.AUTH_USER_MODEL = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sent_messages",
                                                         on_delete=models.SET_NULL, null=True)
    recepient: settings.AUTH_USER_MODEL = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="received_messages",
                                                            on_delete=models.SET_NULL, null=True)
    date_sent = models.CharField(max_length=60, default="")
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, default=None, null=True)


class TextMessage(models.Model):
    message_info = models.OneToOneField(
        ChatMessageInfo, on_delete=models.CASCADE)
    text_message = models.CharField(max_length=300, default="")


def get_media_chat_upload_path(instance, filename):
    return f"{instance.message_info.sender.username}/{instance.message_info.recepient.username}/" \
        + f"{instance.message_info.date_sent}/{filename}"


class ImageMessage(models.Model):
    message_info = models.OneToOneField(
        ChatMessageInfo, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_media_chat_upload_path)


class VoiceMessage(models.Model):
    message_info = models.OneToOneField(
        ChatMessageInfo, on_delete=models.CASCADE)
    audio = models.FileField(upload_to=get_media_chat_upload_path)
