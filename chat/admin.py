from django.contrib import admin

from . import models


# Register your models here.
class ChatMessageInfoInline(admin.TabularInline):
    model = models.ChatMessageInfo


@admin.register(models.Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    inlines = [
        ChatMessageInfoInline
    ]


admin.site.register(models.ChatMessageInfo)
admin.site.register(models.TextMessage)
admin.site.register(models.VoiceMessage)
admin.site.register(models.ImageMessage)
