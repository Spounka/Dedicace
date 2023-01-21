from django.urls import path
from . import views

urlpatterns = [
    path('discussions/', views.DiscussionAPIView.as_view(), name="discussions"),
    path('discussions/<int:pk>/', views.DiscussionAPIView.as_view(), name="discussion"),
    path('text/<int:pk>/', views.TextMessageAPIView.as_view(), name='text-chat'),
    path('voice/<int:pk>/', views.VoiceMessageAPIView.as_view(), name='voice-chat'),
    path('image/<int:pk>/', views.ImageMessageAPIView.as_view(), name='image-chat'),
]
