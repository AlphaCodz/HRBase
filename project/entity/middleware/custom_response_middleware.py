# custom_response_middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from rest_framework.views import exception_handler

class CustomResponseMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Check if it's an error (e.g., 4xx or 5xx)
        if 200 <= response.status_code < 300:
            status = "success"
            message = "Request Successful"
            data = response.data if hasattr(response, 'data') else {}
        else:
            status = "error"
            message = response.reason_phrase or "An error occurred"
            data = response.data if hasattr(response, 'data') else {}

        # Build the custom response structure
        custom_response = {
            'status': status,
            'message': message,
            'data': data
        }

        # Return the custom formatted response as a JsonResponse
        return JsonResponse(custom_response, status=response.status_code)
    
    def process_exception(self, request, exception):
        # Handle exceptions and return as a custom JSON response
        response = exception_handler(exception, None)
        if response is not None:
            return self.process_response(request, response)
        
        # For non-DRF handled exceptions
        return JsonResponse({
            'status': 'error',
            'message': str(exception),
            'data': {}
        }, status=500)
