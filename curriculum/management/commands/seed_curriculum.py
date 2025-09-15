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
        
        # Create Mobile App Development course
        self.stdout.write('Creating Mobile App Development course...')
        mobile_course = self.create_mobile_course()
        mobile_phases = self.create_mobile_phases(mobile_course)
        self.create_mobile_lessons(mobile_phases)
        self.create_cohort(mobile_course, 'Mobile App Development - January 2024')
        
        # Create Cyber Security course
        self.stdout.write('Creating Cyber Security course...')
        cyber_course = self.create_cyber_course()
        cyber_phases = self.create_cyber_phases(cyber_course)
        self.create_cyber_lessons(cyber_phases)
        self.create_cohort(cyber_course, 'Cyber Security - January 2024')
        
        # Create Data Science & Analytics course
        self.stdout.write('Creating Data Science & Analytics course...')
        data_course = self.create_data_science_course()
        data_phases = self.create_data_science_phases(data_course)
        self.create_data_science_lessons(data_phases)
        self.create_cohort(data_course, 'Data Science & Analytics - January 2024')
        
        # Create Cloud Computing course
        self.stdout.write('Creating Cloud Computing course...')
        cloud_course = self.create_cloud_computing_course()
        cloud_phases = self.create_cloud_computing_phases(cloud_course)
        self.create_cloud_computing_lessons(cloud_phases)
        self.create_cohort(cloud_course, 'Cloud Computing - January 2024')
        
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

    def create_mobile_course(self):
        """Create the Mobile App Development course"""
        course, created = Course.objects.get_or_create(
            slug='mobile-app-development',
            defaults={
                'name': 'Mobile App Development',
                'description': 'Learn to build iOS and Android apps using React Native and Flutter. Master mobile development fundamentals, UI/UX design, and app deployment.',
                'duration_months': 8,
                'price_per_phase': 2500.00,
                'is_active': True,
                'is_featured': True,
            }
        )
        
        if created:
            self.stdout.write(f'Created course: {course.name}')
        else:
            self.stdout.write(f'Course already exists: {course.name}')
            
        return course

    def create_cyber_course(self):
        """Create the Cyber Security course"""
        course, created = Course.objects.get_or_create(
            slug='cyber-security',
            defaults={
                'name': 'Cyber Security',
                'description': 'Master cybersecurity fundamentals, ethical hacking, network security, and threat analysis. Learn to protect systems and data from cyber threats.',
                'duration_months': 12,
                'price_per_phase': 4000.00,
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

    def create_mobile_phases(self, course):
        """Create all phases for the Mobile App Development course"""
        phases_data = [
            {
                'phase_number': 1,
                'name': 'Mobile Development Fundamentals',
                'description': 'Learn mobile app concepts, platform differences, and development environment setup.',
                'duration_days': 30,
                'prerequisites': []
            },
            {
                'phase_number': 2,
                'name': 'React Native Basics',
                'description': 'Master React Native components, navigation, and state management.',
                'duration_days': 30,
                'prerequisites': [1]
            },
            {
                'phase_number': 3,
                'name': 'Flutter Development',
                'description': 'Learn Flutter framework, widgets, and cross-platform development.',
                'duration_days': 30,
                'prerequisites': [1]
            },
            {
                'phase_number': 4,
                'name': 'Mobile UI/UX Design',
                'description': 'Design beautiful and intuitive mobile interfaces.',
                'duration_days': 30,
                'prerequisites': [2, 3]
            },
            {
                'phase_number': 5,
                'name': 'Backend Integration',
                'description': 'Connect mobile apps to APIs and handle data synchronization.',
                'duration_days': 30,
                'prerequisites': [2, 3]
            },
            {
                'phase_number': 6,
                'name': 'App Deployment',
                'description': 'Publish apps to App Store and Google Play Store.',
                'duration_days': 30,
                'prerequisites': [4, 5]
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

    def create_cyber_phases(self, course):
        """Create all phases for the Cyber Security course"""
        phases_data = [
            {
                'phase_number': 1,
                'name': 'Cybersecurity Fundamentals',
                'description': 'Learn security concepts, threats, vulnerabilities, and risk management.',
                'duration_days': 30,
                'prerequisites': []
            },
            {
                'phase_number': 2,
                'name': 'Network Security',
                'description': 'Master network protocols, firewalls, and intrusion detection systems.',
                'duration_days': 30,
                'prerequisites': [1]
            },
            {
                'phase_number': 3,
                'name': 'Ethical Hacking',
                'description': 'Learn penetration testing, vulnerability assessment, and ethical hacking techniques.',
                'duration_days': 45,
                'prerequisites': [1, 2]
            },
            {
                'phase_number': 4,
                'name': 'Cryptography',
                'description': 'Understand encryption, digital signatures, and cryptographic protocols.',
                'duration_days': 30,
                'prerequisites': [1]
            },
            {
                'phase_number': 5,
                'name': 'Incident Response',
                'description': 'Learn to detect, analyze, and respond to security incidents.',
                'duration_days': 30,
                'prerequisites': [2, 3]
            },
            {
                'phase_number': 6,
                'name': 'Security Operations',
                'description': 'Implement security monitoring, logging, and compliance frameworks.',
                'duration_days': 30,
                'prerequisites': [3, 4, 5]
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

    def create_mobile_lessons(self, phases):
        """Create sample lessons for Mobile App Development phases"""
        lessons_data = {
            1: [  # Mobile Development Fundamentals
                {'day': 1, 'title': 'Introduction to Mobile Development', 'description': 'Mobile platforms, app types, and development approaches'},
                {'day': 2, 'title': 'Development Environment Setup', 'description': 'Setting up React Native and Flutter development environments'},
                {'day': 3, 'title': 'Mobile App Architecture', 'description': 'Understanding mobile app structure and design patterns'},
                {'day': 4, 'title': 'Platform Differences', 'description': 'iOS vs Android differences and considerations'},
                {'day': 5, 'title': 'Mobile UI Principles', 'description': 'Touch interfaces, gestures, and mobile UX best practices'},
                {'day': 6, 'title': 'Performance Considerations', 'description': 'Mobile performance optimization and memory management'},
                {'day': 7, 'title': 'Mobile Project Setup', 'description': 'Create your first mobile app project'},
            ],
            2: [  # React Native Basics
                {'day': 1, 'title': 'React Native Introduction', 'description': 'Components, JSX, and React Native basics'},
                {'day': 2, 'title': 'Navigation in React Native', 'description': 'React Navigation and screen management'},
                {'day': 3, 'title': 'State Management', 'description': 'useState, useEffect, and Context API'},
                {'day': 4, 'title': 'Styling and Layout', 'description': 'StyleSheet, Flexbox, and responsive design'},
                {'day': 5, 'title': 'Native Modules', 'description': 'Accessing device features and native functionality'},
                {'day': 6, 'title': 'React Native Project', 'description': 'Build a complete React Native app'},
                {'day': 7, 'title': 'Testing and Debugging', 'description': 'Testing strategies and debugging tools'},
            ],
            3: [  # Flutter Development
                {'day': 1, 'title': 'Flutter Introduction', 'description': 'Widgets, Dart language, and Flutter basics'},
                {'day': 2, 'title': 'Flutter Widgets', 'description': 'StatelessWidget, StatefulWidget, and common widgets'},
                {'day': 3, 'title': 'Navigation and Routing', 'description': 'Navigator, Routes, and navigation patterns'},
                {'day': 4, 'title': 'State Management', 'description': 'Provider, Bloc, and state management patterns'},
                {'day': 5, 'title': 'Flutter UI Design', 'description': 'Material Design, Cupertino, and custom themes'},
                {'day': 6, 'title': 'Flutter Project', 'description': 'Build a complete Flutter app'},
                {'day': 7, 'title': 'Flutter Testing', 'description': 'Unit testing, widget testing, and integration testing'},
            ],
            4: [  # Mobile UI/UX Design
                {'day': 1, 'title': 'Mobile Design Principles', 'description': 'Touch targets, accessibility, and mobile-first design'},
                {'day': 2, 'title': 'Design Systems', 'description': 'Creating consistent design systems for mobile apps'},
                {'day': 3, 'title': 'Prototyping Tools', 'description': 'Figma, Sketch, and mobile prototyping'},
                {'day': 4, 'title': 'User Research', 'description': 'User personas, user journeys, and usability testing'},
                {'day': 5, 'title': 'Animation and Interactions', 'description': 'Micro-interactions and smooth animations'},
                {'day': 6, 'title': 'Design Project', 'description': 'Design a complete mobile app interface'},
                {'day': 7, 'title': 'Design Handoff', 'description': 'Handing off designs to developers'},
            ],
            5: [  # Backend Integration
                {'day': 1, 'title': 'API Integration', 'description': 'REST APIs, HTTP requests, and data fetching'},
                {'day': 2, 'title': 'Authentication', 'description': 'JWT tokens, OAuth, and secure authentication'},
                {'day': 3, 'title': 'Data Persistence', 'description': 'Local storage, SQLite, and data synchronization'},
                {'day': 4, 'title': 'Real-time Features', 'description': 'WebSockets, push notifications, and real-time updates'},
                {'day': 5, 'title': 'Offline Support', 'description': 'Offline-first architecture and data caching'},
                {'day': 6, 'title': 'Backend Integration Project', 'description': 'Connect your app to a real backend'},
                {'day': 7, 'title': 'Error Handling', 'description': 'Robust error handling and user feedback'},
            ],
            6: [  # App Deployment
                {'day': 1, 'title': 'App Store Preparation', 'description': 'App store guidelines, metadata, and assets'},
                {'day': 2, 'title': 'iOS App Store', 'description': 'Apple Developer account, certificates, and App Store Connect'},
                {'day': 3, 'title': 'Google Play Store', 'description': 'Google Play Console, app signing, and store listing'},
                {'day': 4, 'title': 'App Store Optimization', 'description': 'ASO strategies, keywords, and app discovery'},
                {'day': 5, 'title': 'Beta Testing', 'description': 'TestFlight, Google Play Internal Testing, and feedback'},
                {'day': 6, 'title': 'App Launch', 'description': 'Launch strategy, marketing, and user acquisition'},
                {'day': 7, 'title': 'Post-Launch', 'description': 'Analytics, updates, and app maintenance'},
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
                        'has_knowledge_check': lesson_data['day'] % 3 == 0,
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

    def create_cyber_lessons(self, phases):
        """Create sample lessons for Cyber Security phases"""
        lessons_data = {
            1: [  # Cybersecurity Fundamentals
                {'day': 1, 'title': 'Introduction to Cybersecurity', 'description': 'Security concepts, threat landscape, and security frameworks'},
                {'day': 2, 'title': 'Threats and Vulnerabilities', 'description': 'Common threats, attack vectors, and vulnerability assessment'},
                {'day': 3, 'title': 'Risk Management', 'description': 'Risk assessment, mitigation strategies, and security policies'},
                {'day': 4, 'title': 'Security Governance', 'description': 'Security frameworks, compliance, and governance'},
                {'day': 5, 'title': 'Security Awareness', 'description': 'Human factors in security and security training'},
                {'day': 6, 'title': 'Security Fundamentals Project', 'description': 'Create a security assessment report'},
                {'day': 7, 'title': 'Security Documentation', 'description': 'Security policies, procedures, and documentation'},
            ],
            2: [  # Network Security
                {'day': 1, 'title': 'Network Fundamentals', 'description': 'TCP/IP, network protocols, and network architecture'},
                {'day': 2, 'title': 'Firewalls and IDS', 'description': 'Firewall configuration, intrusion detection systems'},
                {'day': 3, 'title': 'Network Monitoring', 'description': 'Network traffic analysis and monitoring tools'},
                {'day': 4, 'title': 'VPN and Remote Access', 'description': 'Virtual private networks and secure remote access'},
                {'day': 5, 'title': 'Wireless Security', 'description': 'WiFi security, WPA3, and wireless attack prevention'},
                {'day': 6, 'title': 'Network Security Project', 'description': 'Design and implement network security controls'},
                {'day': 7, 'title': 'Network Hardening', 'description': 'Network device hardening and configuration'},
            ],
            3: [  # Ethical Hacking
                {'day': 1, 'title': 'Ethical Hacking Introduction', 'description': 'Penetration testing methodology and legal considerations'},
                {'day': 2, 'title': 'Reconnaissance', 'description': 'Information gathering, OSINT, and footprinting'},
                {'day': 3, 'title': 'Scanning and Enumeration', 'description': 'Port scanning, service enumeration, and vulnerability scanning'},
                {'day': 4, 'title': 'System Hacking', 'description': 'Password attacks, privilege escalation, and system compromise'},
                {'day': 5, 'title': 'Web Application Testing', 'description': 'OWASP Top 10, web vulnerabilities, and testing tools'},
                {'day': 6, 'title': 'Social Engineering', 'description': 'Social engineering attacks and prevention'},
                {'day': 7, 'title': 'Penetration Testing Project', 'description': 'Conduct a complete penetration test'},
            ],
            4: [  # Cryptography
                {'day': 1, 'title': 'Cryptography Fundamentals', 'description': 'Encryption, decryption, and cryptographic algorithms'},
                {'day': 2, 'title': 'Symmetric Encryption', 'description': 'AES, DES, and symmetric key cryptography'},
                {'day': 3, 'title': 'Asymmetric Encryption', 'description': 'RSA, ECC, and public key cryptography'},
                {'day': 4, 'title': 'Hash Functions', 'description': 'SHA, MD5, and cryptographic hash functions'},
                {'day': 5, 'title': 'Digital Signatures', 'description': 'Digital certificates, PKI, and certificate authorities'},
                {'day': 6, 'title': 'Cryptography Project', 'description': 'Implement cryptographic solutions'},
                {'day': 7, 'title': 'Cryptographic Protocols', 'description': 'SSL/TLS, IPSec, and secure communication protocols'},
            ],
            5: [  # Incident Response
                {'day': 1, 'title': 'Incident Response Planning', 'description': 'Incident response lifecycle and planning'},
                {'day': 2, 'title': 'Detection and Analysis', 'description': 'Threat detection, log analysis, and incident classification'},
                {'day': 3, 'title': 'Containment and Eradication', 'description': 'Incident containment strategies and threat removal'},
                {'day': 4, 'title': 'Recovery and Lessons Learned', 'description': 'System recovery and post-incident analysis'},
                {'day': 5, 'title': 'Forensics', 'description': 'Digital forensics, evidence collection, and analysis'},
                {'day': 6, 'title': 'Incident Response Project', 'description': 'Simulate and respond to a security incident'},
                {'day': 7, 'title': 'Communication and Reporting', 'description': 'Incident communication and reporting procedures'},
            ],
            6: [  # Security Operations
                {'day': 1, 'title': 'Security Operations Center', 'description': 'SOC operations, monitoring, and alerting'},
                {'day': 2, 'title': 'SIEM and Log Management', 'description': 'Security information and event management'},
                {'day': 3, 'title': 'Threat Intelligence', 'description': 'Threat intelligence feeds and analysis'},
                {'day': 4, 'title': 'Compliance and Auditing', 'description': 'Security compliance frameworks and auditing'},
                {'day': 5, 'title': 'Security Automation', 'description': 'SOAR, security orchestration, and automation'},
                {'day': 6, 'title': 'Security Operations Project', 'description': 'Design and implement security operations'},
                {'day': 7, 'title': 'Career Preparation', 'description': 'Security certifications and career paths'},
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
                        'has_knowledge_check': lesson_data['day'] % 3 == 0,
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

    def create_cohort(self, course, cohort_name=None):
        """Create a sample cohort"""
        # Create a cohort starting next month
        start_date = date.today() + timedelta(days=30)
        end_date = start_date + timedelta(days=course.duration_months * 30)
        
        if cohort_name is None:
            cohort_name = 'January 2024 Cohort'
        
        cohort, created = Cohort.objects.get_or_create(
            course=course,
            name=cohort_name,
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

    def create_data_science_course(self):
        """Create the Data Science & Analytics course"""
        course, created = Course.objects.get_or_create(
            slug='data-science-analytics',
            defaults={
                'name': 'Data Science & Analytics',
                'description': 'Learn Python, machine learning, and data visualization. Master statistical analysis and predictive modeling.',
                'duration_months': 12,
                'price_per_phase': 3500.00,
                'is_active': True,
                'is_featured': True,
            }
        )
        if created:
            self.stdout.write(f'Created course: {course.name}')
        else:
            self.stdout.write(f'Course already exists: {course.name}')
        return course

    def create_cloud_computing_course(self):
        """Create the Cloud Computing course"""
        course, created = Course.objects.get_or_create(
            slug='cloud-computing',
            defaults={
                'name': 'Cloud Computing',
                'description': 'Learn AWS, Azure, and Google Cloud platforms for scalable applications. Master cloud architecture and deployment.',
                'duration_months': 8,
                'price_per_phase': 3500.00,
                'is_active': True,
                'is_featured': True,
            }
        )
        if created:
            self.stdout.write(f'Created course: {course.name}')
        else:
            self.stdout.write(f'Course already exists: {course.name}')
        return course

    def create_data_science_phases(self, course):
        """Create phases for Data Science & Analytics course"""
        phases_data = [
            {
                'name': 'Python Fundamentals',
                'description': 'Learn Python programming basics, data types, and control structures',
                'phase_number': 1,
                'duration_days': 28
            },
            {
                'name': 'Data Analysis with Pandas',
                'description': 'Master data manipulation and analysis using Pandas library',
                'phase_number': 2,
                'duration_days': 28
            },
            {
                'name': 'Statistical Analysis',
                'description': 'Learn statistical concepts and hypothesis testing',
                'phase_number': 3,
                'duration_days': 28
            },
            {
                'name': 'Data Visualization',
                'description': 'Create compelling visualizations with Matplotlib and Seaborn',
                'phase_number': 4,
                'duration_days': 28
            },
            {
                'name': 'Machine Learning',
                'description': 'Introduction to machine learning algorithms and models',
                'phase_number': 5,
                'duration_days': 42
            },
            {
                'name': 'Advanced Analytics',
                'description': 'Deep learning, time series analysis, and big data processing',
                'phase_number': 6,
                'duration_days': 42
            }
        ]
        
        phases = []
        for phase_data in phases_data:
            phase, created = Phase.objects.get_or_create(
                course=course,
                phase_number=phase_data['phase_number'],
                defaults=phase_data
            )
            phases.append(phase)
            if created:
                self.stdout.write(f'Created phase: {phase.name}')
        
        return phases

    def create_cloud_computing_phases(self, course):
        """Create phases for Cloud Computing course"""
        phases_data = [
            {
                'name': 'Cloud Fundamentals',
                'description': 'Introduction to cloud computing concepts and service models',
                'phase_number': 1,
                'duration_days': 21
            },
            {
                'name': 'AWS Services',
                'description': 'Learn Amazon Web Services core services and architecture',
                'phase_number': 2,
                'duration_days': 28
            },
            {
                'name': 'Azure Platform',
                'description': 'Microsoft Azure services and cloud solutions',
                'phase_number': 3,
                'duration_days': 28
            },
            {
                'name': 'Google Cloud Platform',
                'description': 'Google Cloud services and data analytics tools',
                'phase_number': 4,
                'duration_days': 28
            },
            {
                'name': 'Cloud Security',
                'description': 'Security best practices and compliance in cloud environments',
                'phase_number': 5,
                'duration_days': 21
            },
            {
                'name': 'DevOps & Automation',
                'description': 'CI/CD pipelines, infrastructure as code, and monitoring',
                'phase_number': 6,
                'duration_days': 28
            }
        ]
        
        phases = []
        for phase_data in phases_data:
            phase, created = Phase.objects.get_or_create(
                course=course,
                phase_number=phase_data['phase_number'],
                defaults=phase_data
            )
            phases.append(phase)
            if created:
                self.stdout.write(f'Created phase: {phase.name}')
        
        return phases
    def create_data_science_lessons(self, phases):
        """Create lessons for Data Science & Analytics course phases"""
        lessons_data = {
            1: [  # Python Fundamentals
                {'title': 'Introduction to Python', 'description': 'Python basics, variables, and data types', 'day_number': 1, 'content': 'Learn Python fundamentals including variables, data types, and basic syntax.'},
                {'title': 'Control Structures', 'description': 'If/else statements, loops, and conditionals', 'day_number': 2, 'content': 'Master conditional statements and loop structures in Python.'},
                {'title': 'Functions and Modules', 'description': 'Creating and using functions, importing modules', 'day_number': 3, 'content': 'Learn to create functions and work with Python modules.'}
            ],
            2: [  # Data Analysis with Pandas
                {'title': 'Pandas Introduction', 'description': 'DataFrames, Series, and basic operations', 'day_number': 1, 'content': 'Learn the fundamentals of Pandas for data manipulation.'},
                {'title': 'Data Loading', 'description': 'Reading CSV, Excel, and JSON files', 'day_number': 2, 'content': 'Master loading data from various file formats.'},
                {'title': 'Data Cleaning', 'description': 'Handling missing values and duplicates', 'day_number': 3, 'content': 'Learn data cleaning techniques and best practices.'}
            ],
            3: [  # Statistical Analysis
                {'title': 'Descriptive Statistics', 'description': 'Mean, median, mode, and standard deviation', 'day_number': 1, 'content': 'Understand basic statistical measures and their applications.'},
                {'title': 'Hypothesis Testing', 'description': 'T-tests, chi-square tests, and p-values', 'day_number': 2, 'content': 'Learn statistical testing methods and interpretation.'},
                {'title': 'Regression Analysis', 'description': 'Linear and multiple regression', 'day_number': 3, 'content': 'Master regression analysis techniques.'}
            ],
            4: [  # Data Visualization
                {'title': 'Matplotlib Basics', 'description': 'Creating basic plots and charts', 'day_number': 1, 'content': 'Learn to create basic visualizations with Matplotlib.'},
                {'title': 'Seaborn Introduction', 'description': 'Statistical data visualization', 'day_number': 2, 'content': 'Explore advanced visualization with Seaborn.'},
                {'title': 'Dashboard Creation', 'description': 'Building data dashboards', 'day_number': 3, 'content': 'Create interactive dashboards for data presentation.'}
            ],
            5: [  # Machine Learning
                {'title': 'ML Introduction', 'description': 'Supervised vs unsupervised learning', 'day_number': 1, 'content': 'Understand the fundamentals of machine learning.'},
                {'title': 'Linear Regression', 'description': 'Simple and multiple linear regression', 'day_number': 2, 'content': 'Implement linear regression models.'},
                {'title': 'Classification', 'description': 'Logistic regression and decision trees', 'day_number': 3, 'content': 'Learn classification algorithms and their applications.'}
            ],
            6: [  # Advanced Analytics
                {'title': 'Deep Learning Basics', 'description': 'Neural networks and TensorFlow', 'day_number': 1, 'content': 'Introduction to deep learning and neural networks.'},
                {'title': 'Time Series Analysis', 'description': 'ARIMA models and forecasting', 'day_number': 2, 'content': 'Learn time series analysis and forecasting techniques.'},
                {'title': 'Capstone Project', 'description': 'Complete data science project', 'day_number': 3, 'content': 'Apply all concepts in a comprehensive data science project.'}
            ]
        }
        
        for phase in phases:
            if phase.phase_number in lessons_data:
                for lesson_data in lessons_data[phase.phase_number]:
                    lesson, created = Lesson.objects.get_or_create(
                        phase=phase,
                        day_number=lesson_data['day_number'],
                        defaults=lesson_data
                    )
                    if created:
                        self.stdout.write(f'Created lesson: {lesson.title}')

    def create_cloud_computing_lessons(self, phases):
        """Create lessons for Cloud Computing course phases"""
        lessons_data = {
            1: [  # Cloud Fundamentals
                {'title': 'Cloud Computing Overview', 'description': 'Introduction to cloud concepts and benefits', 'day_number': 1, 'content': 'Learn the fundamentals of cloud computing and its benefits.'},
                {'title': 'Service Models', 'description': 'IaaS, PaaS, and SaaS explained', 'day_number': 2, 'content': 'Understand different cloud service models and their use cases.'},
                {'title': 'Cloud Security Basics', 'description': 'Shared responsibility model', 'day_number': 3, 'content': 'Learn cloud security fundamentals and shared responsibility.'}
            ],
            2: [  # AWS Services
                {'title': 'AWS Account Setup', 'description': 'Creating and configuring AWS accounts', 'day_number': 1, 'content': 'Set up and configure AWS accounts and services.'},
                {'title': 'EC2 Instances', 'description': 'Virtual machines and instance types', 'day_number': 2, 'content': 'Learn to create and manage EC2 instances.'},
                {'title': 'S3 Storage', 'description': 'Object storage and bucket management', 'day_number': 3, 'content': 'Master AWS S3 storage services and bucket management.'}
            ],
            3: [  # Azure Platform
                {'title': 'Azure Portal', 'description': 'Azure management interface', 'day_number': 1, 'content': 'Navigate and use the Azure management portal.'},
                {'title': 'Virtual Machines', 'description': 'Azure VMs and scaling', 'day_number': 2, 'content': 'Create and manage Azure virtual machines.'},
                {'title': 'Azure Storage', 'description': 'Blob, file, and table storage', 'day_number': 3, 'content': 'Learn Azure storage services and data management.'}
            ],
            4: [  # Google Cloud Platform
                {'title': 'GCP Console', 'description': 'Google Cloud management interface', 'day_number': 1, 'content': 'Use the Google Cloud Console effectively.'},
                {'title': 'Compute Engine', 'description': 'Virtual machines and instances', 'day_number': 2, 'content': 'Work with Google Compute Engine instances.'},
                {'title': 'BigQuery', 'description': 'Data warehouse and analytics', 'day_number': 3, 'content': 'Learn BigQuery for data analytics and warehousing.'}
            ],
            5: [  # Cloud Security
                {'title': 'Security Best Practices', 'description': 'Cloud security fundamentals', 'day_number': 1, 'content': 'Implement cloud security best practices.'},
                {'title': 'Network Security', 'description': 'Firewalls, VPNs, and security groups', 'day_number': 2, 'content': 'Configure network security in cloud environments.'},
                {'title': 'Data Encryption', 'description': 'Encryption at rest and in transit', 'day_number': 3, 'content': 'Implement data encryption strategies.'}
            ],
            6: [  # DevOps & Automation
                {'title': 'CI/CD Pipelines', 'description': 'Continuous integration and deployment', 'day_number': 1, 'content': 'Build CI/CD pipelines for cloud applications.'},
                {'title': 'Infrastructure as Code', 'description': 'Terraform and CloudFormation', 'day_number': 2, 'content': 'Manage infrastructure using code and automation.'},
                {'title': 'DevOps Project', 'description': 'Build a complete DevOps pipeline', 'day_number': 3, 'content': 'Create an end-to-end DevOps solution.'}
            ]
        }
        
        for phase in phases:
            if phase.phase_number in lessons_data:
                for lesson_data in lessons_data[phase.phase_number]:
                    lesson, created = Lesson.objects.get_or_create(
                        phase=phase,
                        day_number=lesson_data['day_number'],
                        defaults=lesson_data
                    )
                    if created:
                        self.stdout.write(f'Created lesson: {lesson.title}')
