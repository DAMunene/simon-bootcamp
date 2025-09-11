from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Course, Phase, Lesson, Cohort, StudentEnrollment, StudentProgress


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'duration_months', 'price_per_phase', 'total_price', 'is_active', 'is_featured', 'created_at']
    list_filter = ['is_active', 'is_featured', 'duration_months', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at', 'total_price', 'total_duration_days']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Course Details', {
            'fields': ('duration_months', 'price_per_phase', 'total_price', 'total_duration_days')
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    fields = ['day_number', 'title', 'is_published', 'is_preview', 'has_knowledge_check']
    readonly_fields = ['created_at']


@admin.register(Phase)
class PhaseAdmin(admin.ModelAdmin):
    list_display = ['course', 'phase_number', 'name', 'duration_days', 'lesson_count', 'is_active']
    list_filter = ['course', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'course__name']
    inlines = [LessonInline]
    readonly_fields = ['created_at', 'updated_at', 'lesson_count']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('course', 'phase_number', 'name', 'description')
        }),
        ('Duration & Prerequisites', {
            'fields': ('duration_days', 'prerequisites')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'phase', 'day_number', 'course', 'is_published', 'has_knowledge_check']
    list_filter = ['phase__course', 'is_published', 'has_knowledge_check', 'created_at']
    search_fields = ['title', 'description', 'content', 'phase__name', 'phase__course__name']
    readonly_fields = ['created_at', 'updated_at', 'course']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('phase', 'day_number', 'title', 'description', 'course')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Knowledge Check', {
            'fields': ('has_knowledge_check', 'knowledge_check_questions')
        }),
        ('Status', {
            'fields': ('is_published',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class StudentEnrollmentInline(admin.TabularInline):
    model = StudentEnrollment
    extra = 0
    fields = ['user', 'status', 'enrollment_date', 'current_phase']
    readonly_fields = ['enrollment_date']


@admin.register(Cohort)
class CohortAdmin(admin.ModelAdmin):
    list_display = ['name', 'course', 'start_date', 'end_date', 'status', 'current_students_count', 'max_students', 'is_accepting_enrollments']
    list_filter = ['course', 'status', 'start_date', 'created_at']
    search_fields = ['name', 'course__name']
    inlines = [StudentEnrollmentInline]
    readonly_fields = ['created_at', 'updated_at', 'current_students_count', 'is_accepting_enrollments']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('course', 'name', 'start_date', 'end_date')
        }),
        ('Capacity & Status', {
            'fields': ('max_students', 'current_students_count', 'status', 'is_accepting_enrollments')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(StudentEnrollment)
class StudentEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'cohort', 'status', 'enrollment_date', 'current_phase', 'current_lesson']
    list_filter = ['status', 'cohort__course', 'cohort', 'enrollment_date']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'cohort__name']
    readonly_fields = ['enrollment_date', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Enrollment Details', {
            'fields': ('user', 'cohort', 'status', 'enrollment_date')
        }),
        ('Progress Tracking', {
            'fields': ('current_phase', 'current_lesson')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(StudentProgress)
class StudentProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'is_completed', 'completion_date', 'knowledge_check_score']
    list_filter = ['is_completed', 'lesson__phase__course', 'completion_date', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'lesson__title']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Progress Details', {
            'fields': ('user', 'lesson', 'is_completed', 'completion_date')
        }),
        ('Knowledge Check Results', {
            'fields': ('knowledge_check_score',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
