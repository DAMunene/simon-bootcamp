from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from curriculum.models import Course, Cohort, StudentEnrollment, StudentProgress, Lesson
from datetime import date, timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed the database with sample students and enrollments'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing student data before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing student data...')
            StudentProgress.objects.all().delete()
            StudentEnrollment.objects.all().delete()
            User.objects.filter(role='student').delete()
            self.stdout.write(
                self.style.SUCCESS('Existing student data cleared.')
            )

        self.stdout.write('Creating sample students...')
        
        # Get the course and cohort
        try:
            course = Course.objects.get(slug='software-engineering-bootcamp')
            cohort = Cohort.objects.filter(course=course).first()
            
            if not cohort:
                self.stdout.write(
                    self.style.ERROR('No cohort found. Please run seed_curriculum first.')
                )
                return
                
        except Course.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Software Engineering course not found. Please run seed_curriculum first.')
            )
            return

        # Create sample students
        students_data = [
            {
                'email': 'john.doe@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'phone_number': '+254712345678',
                'progress_level': 'beginner'  # Just started
            },
            {
                'email': 'jane.smith@example.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'phone_number': '+254723456789',
                'progress_level': 'intermediate'  # Halfway through Phase 1
            },
            {
                'email': 'mike.johnson@example.com',
                'first_name': 'Mike',
                'last_name': 'Johnson',
                'phone_number': '+254734567890',
                'progress_level': 'advanced'  # Completed Phase 1, starting Phase 2
            },
            {
                'email': 'sarah.wilson@example.com',
                'first_name': 'Sarah',
                'last_name': 'Wilson',
                'phone_number': '+254745678901',
                'progress_level': 'expert'  # Completed multiple phases
            },
            {
                'email': 'david.brown@example.com',
                'first_name': 'David',
                'last_name': 'Brown',
                'phone_number': '+254756789012',
                'progress_level': 'beginner'
            }
        ]

        for student_data in students_data:
            student, created = User.objects.get_or_create(
                email=student_data['email'],
                defaults={
                    'first_name': student_data['first_name'],
                    'last_name': student_data['last_name'],
                    'phone_number': student_data['phone_number'],
                    'role': 'student',
                }
            )
            
            if created:
                student.set_password('password123')  # Default password for demo
                student.save()
                self.stdout.write(f'Created student: {student.get_full_name()}')
            else:
                self.stdout.write(f'Student already exists: {student.get_full_name()}')

            # Create enrollment
            enrollment, created = StudentEnrollment.objects.get_or_create(
                user=student,
                cohort=cohort,
                defaults={
                    'status': 'active',
                }
            )
            
            if created:
                self.stdout.write(f'Enrolled student: {student.get_full_name()}')
            
            # Set progress based on level
            self.set_student_progress(student, course, student_data['progress_level'])

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded student data!')
        )

    def set_student_progress(self, student, course, progress_level):
        """Set student progress based on their level"""
        phases = course.phases.all().order_by('phase_number')
        
        if progress_level == 'beginner':
            # Just started - completed first 2 lessons of Phase 1
            phase = phases[0]
            lessons = phase.lessons.filter(is_published=True).order_by('day_number')[:2]
            current_phase = phase
            current_lesson = phase.lessons.filter(is_published=True).order_by('day_number')[2] if phase.lessons.count() > 2 else None
            
        elif progress_level == 'intermediate':
            # Halfway through Phase 1 - completed 4 lessons
            phase = phases[0]
            lessons = phase.lessons.filter(is_published=True).order_by('day_number')[:4]
            current_phase = phase
            current_lesson = phase.lessons.filter(is_published=True).order_by('day_number')[4] if phase.lessons.count() > 4 else None
            
        elif progress_level == 'advanced':
            # Completed Phase 1, starting Phase 2
            phase1 = phases[0]
            phase2 = phases[1]
            lessons = list(phase1.lessons.filter(is_published=True)) + list(phase2.lessons.filter(is_published=True)[:2])
            current_phase = phase2
            current_lesson = phase2.lessons.filter(is_published=True).order_by('day_number')[2] if phase2.lessons.count() > 2 else None
            
        elif progress_level == 'expert':
            # Completed Phase 1 and 2, halfway through Phase 3
            phase1 = phases[0]
            phase2 = phases[1]
            phase3 = phases[2]
            lessons = list(phase1.lessons.filter(is_published=True)) + list(phase2.lessons.filter(is_published=True)) + list(phase3.lessons.filter(is_published=True)[:4])
            current_phase = phase3
            current_lesson = phase3.lessons.filter(is_published=True).order_by('day_number')[4] if phase3.lessons.count() > 4 else None
        
        # Create progress records for completed lessons
        for lesson in lessons:
            progress, created = StudentProgress.objects.get_or_create(
                user=student,
                lesson=lesson,
                defaults={
                    'is_completed': True,
                    'completion_date': self.get_random_completion_date(),
                    'knowledge_check_score': random.uniform(70, 95) if lesson.has_knowledge_check else None,
                }
            )
            
            if created:
                self.stdout.write(f'  Created progress for: {lesson.title}')
        
        # Update enrollment with current phase and lesson
        enrollment = StudentEnrollment.objects.get(user=student, cohort__course=course)
        enrollment.current_phase = current_phase
        enrollment.current_lesson = current_lesson
        enrollment.save()
        
        self.stdout.write(f'  Set current phase: {current_phase.name}')
        if current_lesson:
            self.stdout.write(f'  Set current lesson: {current_lesson.title}')

    def get_random_completion_date(self):
        """Generate a random completion date within the last 30 days"""
        from django.utils import timezone
        import random
        
        now = timezone.now()
        days_ago = random.randint(1, 30)
        return now - timedelta(days=days_ago)
