from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Course


def courses_list(request):
    """
    Display all courses with pagination (12 courses per page)
    """
    # Get search query
    search_query = request.GET.get('search', '')
    
    # Get all courses
    courses = Course.objects.all()
    
    # Filter courses if search query exists
    if search_query:
        courses = courses.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Order courses by name
    courses = courses.order_by('name')
    
    # Paginate courses (12 per page)
    paginator = Paginator(courses, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'total_courses': courses.count(),
    }
    
    return render(request, 'curriculum/courses_list.html', context)


def course_detail(request, slug):
    """
    Display individual course details
    """
    course = get_object_or_404(Course, slug=slug)
    phases = course.phases.all().order_by('phase_number')
    
    context = {
        'course': course,
        'phases': phases,
    }
    
    return render(request, 'curriculum/course_detail.html', context)