from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from curriculum.models import Course, Phase, Lesson, Cohort
from authentication.models import User


class Command(BaseCommand):
    help = 'Seed the database with sample curriculum data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Course.objects.all().delete()
            self.stdout.write(
                self.style.SUCCESS('Existing data cleared.')
            )

        self.stdout.write('Creating Software Engineering Bootcamp...')
        
        # Create the main course
        course = self.create_course()
        
        # Create phases
        phases = self.create_phases(course)
        
        # Create lessons for each phase
        self.create_lessons(phases)
        
        # Create a sample cohort
        self.create_cohort(course)
        
        self.stdout.write(
            self.style.SUCCESS('Successfully seeded curriculum data!')
        )

    def create_course(self):
        """Create the Software Engineering course"""
        course, created = Course.objects.get_or_create(
            slug='software-engineering-bootcamp',
            defaults={
                'name': 'Software Engineering Bootcamp',
                'description': 'Complete full-stack development program covering frontend, backend, and deployment. Learn modern web development technologies and build real-world projects.',
                'duration_months': 10,
                'price_per_phase': 3000.00,
                'is_active': True,
                'is_featured': True,
            }
        )
        
        if created:
            self.stdout.write(f'Created course: {course.name}')
        else:
            self.stdout.write(f'Course already exists: {course.name}')
            
        return course

    def create_phases(self, course):
        """Create all phases for the course"""
        phases_data = [
            {
                'phase_number': 1,
                'name': 'Programming Fundamentals',
                'description': 'Learn basic programming concepts, variables, loops, functions, and problem-solving techniques.',
                'duration_days': 30,
                'prerequisites': []
            },
            {
                'phase_number': 2,
                'name': 'Object-Oriented Programming',
                'description': 'Master classes, objects, inheritance, polymorphism, and design patterns.',
                'duration_days': 30,
                'prerequisites': [1]  # Requires Phase 1
            },
            {
                'phase_number': 3,
                'name': 'Web Development Basics',
                'description': 'Learn HTML, CSS, JavaScript fundamentals, and responsive web design.',
                'duration_days': 30,
                'prerequisites': [1]  # Requires Phase 1
            },
            {
                'phase_number': 4,
                'name': 'Frontend Development',
                'description': 'Build modern web applications with React, state management, and component architecture.',
                'duration_days': 45,
                'prerequisites': [2, 3]  # Requires Phase 2 and 3
            },
            {
                'phase_number': 5,
                'name': 'Backend Development',
                'description': 'Create robust APIs with Node.js, Express, databases, and authentication.',
                'duration_days': 45,
                'prerequisites': [2, 3]  # Requires Phase 2 and 3
            },
            {
                'phase_number': 6,
                'name': 'Full-Stack Integration',
                'description': 'Connect frontend and backend, implement authentication, and deploy applications.',
                'duration_days': 30,
                'prerequisites': [4, 5]  # Requires Phase 4 and 5
            }
        ]
        
        phases = {}
        for phase_data in phases_data:
            phase, created = Phase.objects.get_or_create(
                course=course,
                phase_number=phase_data['phase_number'],
                defaults={
                    'name': phase_data['name'],
                    'description': phase_data['description'],
                    'duration_days': phase_data['duration_days'],
                    'is_active': True,
                }
            )
            
            if created:
                self.stdout.write(f'Created phase: {phase.name}')
            else:
                self.stdout.write(f'Phase already exists: {phase.name}')
                
            phases[phase_data['phase_number']] = phase
        
        # Set up prerequisites
        for phase_data in phases_data:
            phase = phases[phase_data['phase_number']]
            for prereq_num in phase_data['prerequisites']:
                prereq_phase = phases[prereq_num]
                phase.prerequisites.add(prereq_phase)
        
        return phases

    def create_lessons(self, phases):
        """Create sample lessons for each phase"""
        lessons_data = {
            1: [  # Programming Fundamentals
                {'day': 1, 'title': 'Introduction to Programming', 'description': 'What is programming? Setting up your development environment'},
                {'day': 2, 'title': 'Variables and Data Types', 'description': 'Learn about variables, strings, numbers, booleans'},
                {'day': 3, 'title': 'Control Structures', 'description': 'if/else statements, loops, and conditional logic'},
                {'day': 4, 'title': 'Functions', 'description': 'Creating and using functions, parameters, and return values'},
                {'day': 5, 'title': 'Arrays and Lists', 'description': 'Working with collections of data'},
                {'day': 6, 'title': 'Problem Solving', 'description': 'Algorithm thinking and debugging techniques'},
                {'day': 7, 'title': 'Code Review', 'description': 'Review and practice with coding challenges'},
            ],
            2: [  # Object-Oriented Programming
                {'day': 1, 'title': 'Introduction to OOP', 'description': 'Classes, objects, and the four pillars of OOP'},
                {'day': 2, 'title': 'Classes and Objects', 'description': 'Creating classes, instantiation, and methods'},
                {'day': 3, 'title': 'Inheritance', 'description': 'Extending classes and method overriding'},
                {'day': 4, 'title': 'Polymorphism', 'description': 'Method overloading and dynamic binding'},
                {'day': 5, 'title': 'Encapsulation', 'description': 'Access modifiers and data hiding'},
                {'day': 6, 'title': 'Design Patterns', 'description': 'Common OOP design patterns'},
                {'day': 7, 'title': 'OOP Project', 'description': 'Build a project using OOP principles'},
            ],
            3: [  # Web Development Basics
                {'day': 1, 'title': 'HTML Fundamentals', 'description': 'Structure, tags, and semantic HTML'},
                {'day': 2, 'title': 'CSS Styling', 'description': 'Selectors, properties, and layout techniques'},
                {'day': 3, 'title': 'Responsive Design', 'description': 'Media queries and mobile-first design'},
                {'day': 4, 'title': 'JavaScript Basics', 'description': 'Variables, functions, and DOM manipulation'},
                {'day': 5, 'title': 'Event Handling', 'description': 'User interactions and event listeners'},
                {'day': 6, 'title': 'Web Project', 'description': 'Build a responsive website'},
                {'day': 7, 'title': 'Code Review', 'description': 'Review and optimize your web project'},
            ],
            4: [  # Frontend Development
                {'day': 1, 'title': 'React Introduction', 'description': 'Components, JSX, and React basics'},
                {'day': 2, 'title': 'State Management', 'description': 'useState, useEffect, and component state'},
                {'day': 3, 'title': 'Props and Data Flow', 'description': 'Passing data between components'},
                {'day': 4, 'title': 'React Router', 'description': 'Navigation and routing in React apps'},
                {'day': 5, 'title': 'API Integration', 'description': 'Fetching data from external APIs'},
                {'day': 6, 'title': 'State Management Libraries', 'description': 'Redux or Context API'},
                {'day': 7, 'title': 'Frontend Project', 'description': 'Build a complete React application'},
            ],
            5: [  # Backend Development
                {'day': 1, 'title': 'Node.js Introduction', 'description': 'Server-side JavaScript and npm'},
                {'day': 2, 'title': 'Express Framework', 'description': 'Creating REST APIs with Express'},
                {'day': 3, 'title': 'Database Integration', 'description': 'Working with databases (MongoDB/PostgreSQL)'},
                {'day': 4, 'title': 'Authentication', 'description': 'JWT tokens and user authentication'},
                {'day': 5, 'title': 'API Design', 'description': 'RESTful API best practices'},
                {'day': 6, 'title': 'Testing', 'description': 'Unit and integration testing'},
                {'day': 7, 'title': 'Backend Project', 'description': 'Build a complete backend API'},
            ],
            6: [  # Full-Stack Integration
                {'day': 1, 'title': 'Full-Stack Architecture', 'description': 'Connecting frontend and backend'},
                {'day': 2, 'title': 'Authentication Flow', 'description': 'Implementing secure user authentication'},
                {'day': 3, 'title': 'Data Management', 'description': 'State management across the stack'},
                {'day': 4, 'title': 'Deployment', 'description': 'Deploying applications to production'},
                {'day': 5, 'title': 'Performance Optimization', 'description': 'Optimizing for speed and scalability'},
                {'day': 6, 'title': 'Final Project', 'description': 'Build and deploy a complete application'},
                {'day': 7, 'title': 'Portfolio Preparation', 'description': 'Prepare your projects for job applications'},
            ]
        }
        
        for phase_num, lessons in lessons_data.items():
            phase = phases[phase_num]
            for lesson_data in lessons:
                lesson, created = Lesson.objects.get_or_create(
                    phase=phase,
                    day_number=lesson_data['day'],
                    defaults={
                        'title': lesson_data['title'],
                        'description': lesson_data['description'],
                        'content': f"This is the content for {lesson_data['title']}. Students will learn about {lesson_data['description'].lower()}.",
                        'is_published': True,
                        'has_knowledge_check': lesson_data['day'] % 3 == 0,  # Every 3rd lesson has a knowledge check
                        'knowledge_check_questions': [
                            {
                                "question": f"What is the main topic of {lesson_data['title']}?",
                                "type": "multiple_choice",
                                "options": ["Option A", "Option B", "Option C", "Option D"],
                                "correct_answer": 0
                            }
                        ] if lesson_data['day'] % 3 == 0 else []
                    }
                )
                
                if created:
                    self.stdout.write(f'Created lesson: {lesson.title}')

    def create_cohort(self, course):
        """Create a sample cohort"""
        # Create a cohort starting next month
        start_date = date.today() + timedelta(days=30)
        end_date = start_date + timedelta(days=course.duration_months * 30)
        
        cohort, created = Cohort.objects.get_or_create(
            course=course,
            name='January 2024 Cohort',
            defaults={
                'start_date': start_date,
                'end_date': end_date,
                'status': 'upcoming',
                'max_students': 50,
            }
        )
        
        if created:
            self.stdout.write(f'Created cohort: {cohort.name}')
        else:
            self.stdout.write(f'Cohort already exists: {cohort.name}')
            
        return cohort
