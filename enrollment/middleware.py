import logging
from django.http import HttpResponseServerError
from django.template.loader import render_to_string
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

logger = logging.getLogger(__name__)

def get_client_ip(request):
    """
    Get the client's IP address from the request
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    """
    Signal handler to update the user's last login IP
    """
    if hasattr(user, 'profile'):
        user.profile.last_login_ip = get_client_ip(request)
        user.profile.save()

class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        # Log the error
        logger.error(f"Unhandled Exception: {str(exception)}", exc_info=True)
        
        # Render the 500 template
        html = render_to_string('500.html', {}, request)
        return HttpResponseServerError(html)

class SecurityMiddleware(MiddlewareMixin):
    """
    Middleware to add security headers to responses
    """
    def process_response(self, request, response):
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'SAMEORIGIN'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Only add HSTS header on HTTPS connections
        if request.is_secure():
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
            
        return response