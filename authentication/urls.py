from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    # Authentication URLs
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    
    # Password Reset URLs (Django built-in)
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset_request'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset-password/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password/complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    # Profile URLs (Login Required)
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/edit/', views.UserProfileEditView.as_view(), name='edit_profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
]
