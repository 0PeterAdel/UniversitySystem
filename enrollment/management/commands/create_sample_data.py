import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from enrollment.models import Department, Student, Course, Enrollment

class Command(BaseCommand):
    help = 'Creates sample data for the SEAS application'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')
        
        # Create departments
        departments = [
            {'code': 'CSE', 'name': 'Computer Science and Engineering'},
            {'code': 'EEE', 'name': 'Electrical and Electronic Engineering'},
            {'code': 'BBA', 'name': 'Business Administration'},
            {'code': 'ECO', 'name': 'Economics'},
            {'code': 'ENG', 'name': 'English'},
        ]
        
        for dept in departments:
            Department.objects.get_or_create(
                code=dept['code'],
                defaults={'name': dept['name']}
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(departments)} departments'))
        
        # Get all departments
        all_departments = Department.objects.all()
        
        # Create courses
        courses = [
            {'course_code': 'CSE101', 'title': 'Introduction to Programming', 'credit_hours': 3, 'department': 'CSE'},
            {'course_code': 'CSE201', 'title': 'Data Structures', 'credit_hours': 3, 'department': 'CSE'},
            {'course_code': 'CSE301', 'title': 'Database Systems', 'credit_hours': 3, 'department': 'CSE'},
            {'course_code': 'CSE401', 'title': 'Artificial Intelligence', 'credit_hours': 3, 'department': 'CSE'},
            {'course_code': 'EEE101', 'title': 'Basic Electrical Engineering', 'credit_hours': 3, 'department': 'EEE'},
            {'course_code': 'EEE201', 'title': 'Digital Logic Design', 'credit_hours': 3, 'department': 'EEE'},
            {'course_code': 'BBA101', 'title': 'Principles of Management', 'credit_hours': 3, 'department': 'BBA'},
            {'course_code': 'BBA201', 'title': 'Financial Accounting', 'credit_hours': 3, 'department': 'BBA'},
            {'course_code': 'ECO101', 'title': 'Principles of Economics', 'credit_hours': 3, 'department': 'ECO'},
            {'course_code': 'ENG101', 'title': 'English Composition', 'credit_hours': 3, 'department': 'ENG'},
        ]
        
        for course in courses:
            dept = Department.objects.get(code=course['department'])
            Course.objects.get_or_create(
                course_code=course['course_code'],
                defaults={
                    'title': course['title'],
                    'credit_hours': course['credit_hours'],
                    'department': dept
                }
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(courses)} courses'))
        
        # Create students
        first_names = ['John', 'Jane', 'Michael', 'Emily', 'David', 'Sarah', 'Robert', 'Lisa', 'William', 'Emma',
                      'James', 'Olivia', 'Daniel', 'Sophia', 'Matthew', 'Ava', 'Joseph', 'Isabella', 'Andrew', 'Mia']
        last_names = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor',
                     'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin', 'Thompson', 'Garcia', 'Martinez', 'Robinson']
        
        # Create 50 students
        for i in range(1, 51):
            student_id = f'2025{i:03d}'
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            email = f'{first_name.lower()}.{last_name.lower()}.{i}@example.com'
            
            # Random date of birth (18-25 years old)
            today = datetime.now().date()
            age = random.randint(18, 25)
            dob = today - timedelta(days=age*365 + random.randint(0, 364))
            
            # Random admission date (within last 4 years)
            years_ago = random.randint(0, 3)
            months_ago = random.randint(0, 11)
            admission_date = today - timedelta(days=years_ago*365 + months_ago*30)
            
            # Random department
            department = random.choice(all_departments)
            
            # Random CGPA (2.0 - 4.0)
            cgpa = round(random.uniform(2.0, 4.0), 2)
            
            # Random gender
            gender = random.choice(['M', 'F'])
            
            Student.objects.get_or_create(
                student_id=student_id,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'date_of_birth': dob,
                    'gender': gender,
                    'department': department,
                    'admission_date': admission_date,
                    'cgpa': cgpa
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Created 50 students'))
        
        # Create enrollments
        all_students = Student.objects.all()
        all_courses = Course.objects.all()
        semesters = ['Spring', 'Summer', 'Fall']
        years = [2023, 2024, 2025]
        
        # Create 200 enrollments
        for _ in range(200):
            student = random.choice(all_students)
            course = random.choice(all_courses)
            semester = random.choice(semesters)
            year = random.choice(years)
            
            # Create enrollment if it doesn't exist
            Enrollment.objects.get_or_create(
                student=student,
                course=course,
                semester=semester,
                year=year
            )
        
        # Count actual enrollments created (might be less than 200 due to uniqueness constraint)
        enrollment_count = Enrollment.objects.count()
        self.stdout.write(self.style.SUCCESS(f'Created {enrollment_count} enrollments'))
        
        self.stdout.write(self.style.SUCCESS('Sample data creation completed!'))