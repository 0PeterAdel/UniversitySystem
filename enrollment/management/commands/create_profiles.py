from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from enrollment.models import UserProfile

class Command(BaseCommand):
    help = 'Create user profiles for existing users'

    def handle(self, *args, **options):
        # Get all users
        users = User.objects.all()
        created_count = 0
        
        for user in users:
            # Check if user already has a profile
            try:
                profile = user.profile
                self.stdout.write(f"User {user.username} already has a profile")
            except UserProfile.DoesNotExist:
                # Create profile for user
                profile = UserProfile.objects.create(user=user)
                created_count += 1
                self.stdout.write(f"Created profile for {user.username}")
        
        # Print summary
        self.stdout.write(self.style.SUCCESS(f"Profile creation complete: {created_count} profiles created"))