from django.shortcuts import redirect
from django.urls import resolve, reverse

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            # Allow password change URLs
            if any(url in request.path for url in [
                '/admin/password_change/',
                '/admin/password_change/done/',
            ]):
                return self.get_response(request)
            
            # Allow specific admin URLs if needed
            allowed_urls = [
                '/admin/auth/user/',  # Only for superusers, but that's handled by the UNFOLD permissions
            ]
            if request.path in allowed_urls:
                return self.get_response(request)
            
            # If it's the admin index, redirect to contacts
            if request.path == '/admin/' or request.path == '/admin':
                return redirect('contacts')
            
            # Block other admin URLs
            return redirect('contacts')

        return self.get_response(request) 