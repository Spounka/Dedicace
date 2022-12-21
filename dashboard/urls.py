from django.urls import path, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('celebs/create/', views.CreateCelebrityAPIView.as_view(), name='dashboard-create-celeb'),
    path('payments/', views.CreateCelebrityAPIView.as_view(), name='dashboard-view-payments'),
    path('users/', views.CreateCelebrityAPIView.as_view(), name='dashboard-view-users'),
    path('reports/', views.CreateCelebrityAPIView.as_view(), name='dashboard-view-reports'),
]
