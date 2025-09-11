from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class TimeStampedModel(models.Model):
    """Abstract base model that provides timestamp fields"""
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        abstract = True


class Course(TimeStampedModel):
    """Main course model for bootcamp programs"""
    
    DURATION_CHOICES = [
        (8, '8 months - Intensive'),
        (9, '9 months'),
        (10, '10 months'),
        (12, '12 months - Relaxed'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='Course Name')
    slug = models.SlugField(unique=True, verbose_name='URL Slug')
    description = models.TextField(verbose_name='Course Description')
    
    # Duration and pricing
    duration_months = models.IntegerField(
        choices=DURATION_CHOICES,
        default=10,
        verbose_name='Duration (months)'
    )
    price_per_phase = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Price per Phase (Ksh)'
    )
    
    # Course status
    is_active = models.BooleanField(default=True, verbose_name='Active')
    is_featured = models.BooleanField(default=False, verbose_name='Featured Course')
    
    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.duration_months} months)"
    
    @property
    def total_price(self):
        """Calculate total course price based on phases"""
        return self.price_per_phase * self.phases.count()
    
    @property
    def total_duration_days(self):
        """Calculate total course duration in days"""
        return sum(phase.duration_days for phase in self.phases.all())


class Phase(TimeStampedModel):
    """Course phases - each phase represents a major learning module"""
    
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='phases',
        verbose_name='Course'
    )
    phase_number = models.PositiveIntegerField(verbose_name='Phase Number')
    name = models.CharField(max_length=100, verbose_name='Phase Name')
    description = models.TextField(verbose_name='Phase Description')
    
    # Duration
    duration_days = models.PositiveIntegerField(
        verbose_name='Duration (days)',
        validators=[MinValueValidator(1), MaxValueValidator(365)]
    )
    
    # Prerequisites
    prerequisites = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='leads_to',
        verbose_name='Prerequisites'
    )
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name='Active')
    
    class Meta:
        verbose_name = 'Phase'
        verbose_name_plural = 'Phases'
        ordering = ['course', 'phase_number']
        unique_together = ['course', 'phase_number']
    
    def __str__(self):
        return f"{self.course.name} - Phase {self.phase_number}: {self.name}"
    
    @property
    def lesson_count(self):
        """Get total number of lessons in this phase"""
        return self.lessons.count()


class Lesson(TimeStampedModel):
    """Individual lessons within a phase"""
    
    phase = models.ForeignKey(
        Phase,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Phase'
    )
    day_number = models.PositiveIntegerField(verbose_name='Day Number')
    title = models.CharField(max_length=200, verbose_name='Lesson Title')
    description = models.TextField(verbose_name='Lesson Description')
    
    # Content
    content = models.TextField(verbose_name='Lesson Content')
    
    # Knowledge checks
    has_knowledge_check = models.BooleanField(default=False, verbose_name='Has Knowledge Check')
    knowledge_check_questions = models.JSONField(default=list, blank=True, verbose_name='Knowledge Check Questions')
    
    # Status
    is_published = models.BooleanField(default=False, verbose_name='Published')
    
    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'
        ordering = ['phase', 'day_number']
        unique_together = ['phase', 'day_number']
    
    def __str__(self):
        return f"Day {self.day_number}: {self.title}"
    
    @property
    def course(self):
        """Get the course this lesson belongs to"""
        return self.phase.course


class Cohort(TimeStampedModel):
    """Student cohorts - groups of students starting together"""
    
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='cohorts',
        verbose_name='Course'
    )
    name = models.CharField(max_length=100, verbose_name='Cohort Name')
    start_date = models.DateField(verbose_name='Start Date')
    end_date = models.DateField(verbose_name='End Date')
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='upcoming',
        verbose_name='Status'
    )
    max_students = models.PositiveIntegerField(
        default=50,
        verbose_name='Maximum Students'
    )
    
    class Meta:
        verbose_name = 'Cohort'
        verbose_name_plural = 'Cohorts'
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.course.name} - {self.name} ({self.start_date})"
    
    @property
    def current_students_count(self):
        """Get current number of enrolled students"""
        return self.enrollments.filter(status='active').count()
    
    @property
    def is_full(self):
        """Check if cohort is at capacity"""
        return self.current_students_count >= self.max_students
    
    @property
    def is_accepting_enrollments(self):
        """Check if cohort is accepting new enrollments"""
        return (
            self.status == 'upcoming' and 
            not self.is_full and 
            self.start_date > timezone.now().date()
        )


class StudentEnrollment(TimeStampedModel):
    """Student enrollment in a cohort"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
        ('suspended', 'Suspended'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='Student'
    )
    cohort = models.ForeignKey(
        Cohort,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='Cohort'
    )
    
    # Enrollment details
    enrollment_date = models.DateTimeField(auto_now_add=True, verbose_name='Enrollment Date')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Status'
    )
    
    # Progress tracking
    current_phase = models.ForeignKey(
        Phase,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Current Phase'
    )
    current_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Current Lesson'
    )
    
    class Meta:
        verbose_name = 'Student Enrollment'
        verbose_name_plural = 'Student Enrollments'
        unique_together = ['user', 'cohort']
        ordering = ['-enrollment_date']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.cohort.name}"
    
    @property
    def course(self):
        """Get the course for this enrollment"""
        return self.cohort.course
    


class StudentProgress(TimeStampedModel):
    """Track student progress through lessons and phases"""
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='progress_records',
        verbose_name='Student'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='progress_records',
        verbose_name='Lesson'
    )
    
    # Progress tracking
    is_completed = models.BooleanField(default=False, verbose_name='Completed')
    completion_date = models.DateTimeField(null=True, blank=True, verbose_name='Completion Date')
    
    # Knowledge check results
    knowledge_check_score = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Knowledge Check Score (%)'
    )
    
    class Meta:
        verbose_name = 'Student Progress'
        verbose_name_plural = 'Student Progress Records'
        unique_together = ['user', 'lesson']
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.lesson.title}"
    
    def save(self, *args, **kwargs):
        """Auto-set completion date when marked as completed"""
        if self.is_completed and not self.completion_date:
            self.completion_date = timezone.now()
        super().save(*args, **kwargs)
