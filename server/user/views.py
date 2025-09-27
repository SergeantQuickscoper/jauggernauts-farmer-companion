from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import json

# Create your views here.

def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email', '')

        if not username or not password:
            return JsonResponse({'error': 'Username and password required'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already taken'}, status=400)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'logged in successfully'}, status=201)

    return JsonResponse({'error': 'Only POST allowed'}, status=405)