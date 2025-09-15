from django.urls import path
from . import views

app_name = 'curriculum'

urlpatterns = [
    path('courses/', views.courses_list, name='courses_list'),
    path('courses/<slug:slug>/', views.course_detail, name='course_detail'),
]