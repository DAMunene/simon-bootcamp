from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('progress/', views.ProgressView.as_view(), name='progress'),
    path('courses/', views.CoursesView.as_view(), name='courses'),
]
