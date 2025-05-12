from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from enrollment.models import UserProfile, Student

class Command(BaseCommand):
    help = 'Assign roles to users based on their status'

    def handle(self, *args, **options):
        # Get all users
        users = User.objects.all()
        
        # Count variables for reporting
        admin_count = 0
        student_count = 0
        guest_count = 0
        
        for user in users:
            # Skip if user already has a role assigned
            if hasattr(user, 'profile') and user.profile.role != 'guest':
                self.stdout.write(f"User {user.username} already has role: {user.profile.role}")
                continue
                
            # Assign admin role to superusers
            if user.is_superuser:
                user.profile.role = 'admin'
                user.profile.save()
                admin_count += 1
                self.stdout.write(f"Assigned admin role to {user.username}")
                
            # Check if user is linked to a student
            elif hasattr(user, 'student'):
                user.profile.role = 'student'
                user.profile.department = user.student.department
                user.profile.save()
                student_count += 1
                self.stdout.write(f"Assigned student role to {user.username}")
                
            # Default to guest role
            else:
                user.profile.role = 'guest'
                user.profile.save()
                guest_count += 1
                self.stdout.write(f"Assigned guest role to {user.username}")
        
        # Link students to users with matching email addresses
        students = Student.objects.filter(user__isnull=True)
        linked_count = 0
        
        for student in students:
            try:
                user = User.objects.get(email=student.email)
                student.user = user
                student.save()
                
                # Update user profile
                user.profile.role = 'student'
                user.profile.department = student.department
                user.profile.save()
                
                linked_count += 1
                self.stdout.write(f"Linked student {student.student_id} to user {user.username}")
            except User.DoesNotExist:
                continue
        
        # Print summary
        self.stdout.write(self.style.SUCCESS(f"Role assignment complete:"))
        self.stdout.write(f"- {admin_count} users assigned admin role")
        self.stdout.write(f"- {student_count} users assigned student role")
        self.stdout.write(f"- {guest_count} users assigned guest role")
        self.stdout.write(f"- {linked_count} students linked to existing users")