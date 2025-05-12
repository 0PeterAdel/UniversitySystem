from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from functools import wraps
from django.contrib import messages

def role_required(roles):
    """
    Decorator for views that checks if the user has the required role.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            # Check if user has a profile
            if not hasattr(request.user, 'profile'):
                messages.error(request, "Your user profile is incomplete. Please contact an administrator.")
                return redirect('login')
            
            # If roles is a string, convert it to a list
            role_list = [roles] if isinstance(roles, str) else roles
            
            # Check if user's role is in the required roles
            if request.user.is_superuser or request.user.profile.role in role_list:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "You don't have permission to access this page.")
                raise PermissionDenied("You don't have permission to access this page.")
                
        return _wrapped_view
    return decorator

def admin_required(view_func):
    """
    Decorator for views that checks if the user is an admin.
    """
    return role_required('admin')(view_func)

def staff_required(view_func):
    """
    Decorator for views that checks if the user is staff.
    """
    return role_required(['admin', 'staff'])(view_func)

def faculty_required(view_func):
    """
    Decorator for views that checks if the user is faculty.
    """
    return role_required(['admin', 'faculty'])(view_func)

def student_required(view_func):
    """
    Decorator for views that checks if the user is a student.
    """
    return role_required(['admin', 'student'])(view_func)