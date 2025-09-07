from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(View):
    """Landing page view for the bootcamp platform"""
    
    def get(self, request):
        return render(request, 'home/landing.html')


class DashboardView(LoginRequiredMixin, View):
    """Student dashboard view"""
    
    def get(self, request):
        context = {
            'title': 'Dashboard',
            'user': request.user,
        }
        return render(request, 'home/dashboard.html', context)