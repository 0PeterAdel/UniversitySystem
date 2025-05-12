import logging
from django.http import HttpResponseServerError
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)

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