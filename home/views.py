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


class ProgressView(LoginRequiredMixin, View):
    """Student progress view"""
    
    def get(self, request):
        # Mock data for progress metrics - in real app, this would come from database
        context = {
            'title': 'Progress',
            'user': request.user,
            'progress_data': {
                'overall_completion': 25,
                'lessons_completed': 15,
                'total_lessons': 60,
                'phases_completed': 1,
                'total_phases': 6,
                'time_spent_hours': 42,
                'learning_streak_days': 7,
                'knowledge_check_average': 87,
                'current_phase_progress': 60,
                'recent_achievements': [
                    {'title': 'First Phase Complete', 'date': '2024-01-20', 'type': 'phase'},
                    {'title': 'Perfect Score', 'date': '2024-01-18', 'type': 'quiz'},
                    {'title': '7-Day Streak', 'date': '2024-01-15', 'type': 'streak'},
                ],
                'phase_progress': [
                    {'name': 'Programming Fundamentals', 'progress': 60, 'status': 'in_progress'},
                    {'name': 'Object-Oriented Programming', 'progress': 0, 'status': 'locked'},
                    {'name': 'Web Development Basics', 'progress': 0, 'status': 'locked'},
                    {'name': 'Database Design', 'progress': 0, 'status': 'locked'},
                    {'name': 'Full-Stack Development', 'progress': 0, 'status': 'locked'},
                    {'name': 'Capstone Project', 'progress': 0, 'status': 'locked'},
                ]
            }
        }
        return render(request, 'home/progress.html', context)


class CoursesView(LoginRequiredMixin, View):
    """Student courses view"""
    
    def get(self, request):
        # Mock data for courses - in real app, this would come from database
        context = {
            'title': 'My Courses',
            'user': request.user,
            'courses_data': {
                'enrolled_courses': [
                    {
                        'id': 1,
                        'title': 'Software Engineering Bootcamp',
                        'description': 'Comprehensive full-stack development program covering modern web technologies',
                        'instructor': 'Dr. Sarah Johnson',
                        'start_date': '2024-01-15',
                        'end_date': '2024-11-15',
                        'progress': 25,
                        'lessons_completed': 15,
                        'total_lessons': 60,
                        'current_phase': 'Programming Fundamentals',
                        'next_lesson': 'Control Structures (if/else)',
                        'status': 'active',
                        'cohort': 'January 2024',
                        'difficulty': 'Intermediate',
                        'estimated_hours': 480,
                        'certificate_available': True,
                        'last_accessed': '2024-01-22',
                        'upcoming_deadlines': [
                            {'title': 'Phase 1 Assessment', 'date': '2024-02-15', 'type': 'assessment'},
                            {'title': 'Mid-term Project', 'date': '2024-04-01', 'type': 'project'},
                        ]
                    }
                ],
                'completed_courses': [],
                'available_courses': [
                    {
                        'id': 2,
                        'title': 'Data Science Fundamentals',
                        'description': 'Learn Python, statistics, and machine learning basics',
                        'instructor': 'Prof. Michael Chen',
                        'duration': '6 months',
                        'difficulty': 'Beginner',
                        'estimated_hours': 240,
                        'price': 'Free',
                        'status': 'available'
                    },
                    {
                        'id': 3,
                        'title': 'Cybersecurity Essentials',
                        'description': 'Introduction to cybersecurity concepts and practices',
                        'instructor': 'Dr. Emily Rodriguez',
                        'duration': '4 months',
                        'difficulty': 'Intermediate',
                        'estimated_hours': 180,
                        'price': '$299',
                        'status': 'available'
                    }
                ]
            }
        }
        return render(request, 'home/courses.html', context)