from django.urls import path

from . import views

urlpatterns = [
    path('discussions/', views.DiscussionAPIView.as_view(), name="discussions"),
    path('discussions/<int:pk>/', views.DiscussionAPIView.as_view(), name="discussion"),
    path('message/', views.MessageInfoAPIView.as_view(), name="message")
]
