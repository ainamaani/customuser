from django.shortcuts import render
from . models import CustomUser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model, authenticate, login, logout
import json

# Create your views here.
@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        print(data)

        # get the data
        email = data.get('email')
        club = data.get('club')
        password = data.get('password')

        if not email or not club or not password:
            return JsonResponse({'error':'Email, club and password is required'}, status=400)
        
        try:
            User = get_user_model()
            user = User.objects.create_user(email=email,
                                            password=password,
                                            club=club
                                            )
            return JsonResponse({'message':'User registered successfully'}, status=202)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

def fetch_all_users(request):
    if request.method == 'GET':
        try:
            users = CustomUser.objects.all()

            # serialize users data
            users_data = [{'email': user.email, 'club': user.club, 'password': user.password} for user in users]

            # Return JSON response
            return JsonResponse({'users': users_data}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error':'Only GET requests are allowed'}, status=500)

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        email = data.get('email')
        password = data.get('password')

        try:
            
            if not email or not password:
                return JsonResponse({'error':'Email and password is required'}, status=400)
            # authenticate user
            user = authenticate(request, email=email, password=password)

            if user is not None:
                # If authentication succeeds, log in the user
                login(request, user)
                return JsonResponse({'message': 'Login successful'}, status=200)
            else:
                # If authentication fails, return error response
                return JsonResponse({'error': 'Invalid email or password'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # If request method is not POST, return error response
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    
@csrf_exempt
def user_logout(request):
    if request.method == 'POST':
        try:
            # Log out the user
            logout(request)
            return JsonResponse({'message': 'Logout successful'}, status=200)
        except Exception as e:
            # If any exception occurs, return error response
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # If request method is not POST, return error response
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)