from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from django.urls import reverse_lazy
import json

from .models import User
from .forms import (
    UserRegistrationForm, 
    UserLoginForm, 
    ChangePasswordForm
)


class UserRegistrationView(View):
    """View for user registration"""
    
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'authentication/register.html', {'form': form})
    
    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, f'Account created successfully for {user.email}')
                return redirect('authentication:login')
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
        
        return render(request, 'authentication/register.html', {'form': form})


class UserLoginView(View):
    """View for user login"""
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('core:dashboard')  # Redirect to dashboard if already logged in
        
        form = UserLoginForm()
        return render(request, 'authentication/login.html', {'form': form})
    
    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                
                messages.success(request, f'Welcome back, {user.get_full_name()}!')
                
                # Redirect to dashboard
                return redirect('home:dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
        
        return render(request, 'authentication/login.html', {'form': form})


class UserLogoutView(View):
    """View for user logout"""
    
    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, f'Goodbye, {request.user.get_full_name()}!')
        logout(request)
        return redirect('authentication:login')


# Django's built-in password reset views
class CustomPasswordResetView(PasswordResetView):
    """Custom password reset view using Django's built-in functionality"""
    template_name = 'authentication/password_reset_request.html'
    email_template_name = 'authentication/password_reset_email.html'
    subject_template_name = 'authentication/password_reset_subject.txt'
    success_url = reverse_lazy('authentication:password_reset_done')
    from_email = 'noreply@bootcamp.com'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reset Password'
        context['site_name'] = 'Bootcamp'
        return context
    
    def form_valid(self, form):
        # Add site_name to the email context
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': {'site_name': 'Bootcamp'},
        }
        form.save(**opts)
        return super().form_valid(form)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """Password reset email sent confirmation"""
    template_name = 'authentication/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Password reset form with token validation"""
    template_name = 'authentication/password_reset.html'
    success_url = reverse_lazy('authentication:password_reset_complete')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Set New Password'
        return context


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """Password reset completed successfully"""
    template_name = 'authentication/password_reset_complete.html'


@method_decorator(login_required, name='dispatch')
class ChangePasswordView(View):
    """View for changing password when logged in"""
    
    def get(self, request):
        form = ChangePasswordForm(user=request.user)
        return render(request, 'authentication/change_password.html', {'form': form})
    
    def post(self, request):
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Password changed successfully.')
                return redirect('core:profile')
            except Exception as e:
                messages.error(request, f'Error changing password: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
        
        return render(request, 'authentication/change_password.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class UserProfileView(View):
    """View for user profile"""
    
    def get(self, request):
        user = request.user
        return render(request, 'authentication/profile.html', {'user': user})


@method_decorator(login_required, name='dispatch')
class UserProfileEditView(View):
    """View for editing user profile"""
    
    def get(self, request):
        user = request.user
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_number': user.phone_number,
            'email': user.email,
        }
        form = UserRegistrationForm(initial=initial_data)
        # Remove password fields for profile edit
        form.fields.pop('password1', None)
        form.fields.pop('password2', None)
        return render(request, 'authentication/edit_profile.html', {'form': form})
    
    def post(self, request):
        user = request.user
        form = UserRegistrationForm(request.POST)
        # Remove password fields for profile edit
        form.fields.pop('password1', None)
        form.fields.pop('password2', None)
        
        if form.is_valid():
            try:
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.phone_number = form.cleaned_data.get('phone_number', '')
                user.save()
                
                messages.success(request, 'Profile updated successfully.')
                return redirect('authentication:profile')
            except Exception as e:
                messages.error(request, f'Error updating profile: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
        
        return render(request, 'authentication/edit_profile.html', {'form': form})
