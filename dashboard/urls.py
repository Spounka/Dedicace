from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='dashboard-index'),
    path('login/', views.AdminLogin.as_view(), name="dashboard-login"),
    path('celebs/create/', views.CreateCelebrityAPIView.as_view(), name='dashboard-create-celeb'),
    path('payments/', views.PaymentsView.as_view(), name='dashboard-view-payments'),
    path('users/', views.CreateCelebrityAPIView.as_view(), name='dashboard-view-users'),
    path('reports/', views.CreateCelebrityAPIView.as_view(), name='dashboard-view-reports'),
    path(r'download/', views.download_file, name='dashboard-download-file')
]
