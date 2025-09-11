from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('progress/', views.ProgressView.as_view(), name='progress'),
    path('courses/', views.CoursesView.as_view(), name='courses'),
]
