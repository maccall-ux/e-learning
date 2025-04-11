# middleware.py
from django.http import HttpResponseForbidden
from django.conf import settings
import re

class PrivateFileAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.private_url_pattern = re.compile(r'^/media/uploads/private/')

    def __call__(self, request):
        response = self.get_response(request)
        
        if (self.private_url_pattern.match(request.path) and 
            not request.user.is_authenticated and
            not request.user.is_superuser):
            return HttpResponseForbidden()
            
        return response