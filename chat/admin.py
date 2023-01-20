from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.Discussion)
admin.site.register(models.ChatMessageInfo)
admin.site.register(models.TextMessage)
admin.site.register(models.VoiceMessage)
admin.site.register(models.ImageMessage)
