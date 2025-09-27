# login for every request
import json
from django.contrib.auth import authenticate, login
class LoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization goes here

    def __call__(self, request):
        login_user(request)

        response = self.get_response(request)
        return response


def login_user(request):
    if not request.path.startswith('/api/'):
        return
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    user = authenticate(request, username=username, password=password)
    login(request, user)

