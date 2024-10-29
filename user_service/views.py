import json
from django.http import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login

#register user
@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            age = data.get('age')
            email = data.get('email')
            contact_no = data.get('contact_no')
            dob = data.get('dob')

            if User.objects.filter(username = username).exists():
                return JsonResponse({'error' : 'Username already exists'}, status=400)
            
            user = User.objects.create_user(username=username, password=password)

            if age or email or contact_no or dob :
                UserProfile.objects.create(
                    user = user,
                    age = age,
                    email = email,
                    contact_no = contact_no,
                    dob = dob
                )

            return JsonResponse({
                'message' : 'User registered Successfully',
                'user_id' : user.id,
                'username' : user.username
            }, status=200)
        except:
            return JsonResponse({'error' : 'Invalid Json Format'}, status=400)
        
    return JsonResponse({'error' : 'Only POST request are allowed'}, status=405)



#login user
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            age = data.get('age')
            email = data.get('email')
            contact_no = data.get('contact_no')
            dob = data.get('dob')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                try:
                    profile = UserProfile.objects.get(user=user)

                    if profile.is_deleted:
                        return JsonResponse({'error' : 'User account is deleted'}, status=400)
                    
                    profile_data = {
                        'age' : profile.age,
                        'email' : profile.email,
                        'contact_no' : profile.contact_no,
                        'dob' : profile.dob
                    }
                except UserProfile.DoesNotExist:
                    profile_data = None

                return JsonResponse({
                    'message' : 'User Login Successful',
                    'username' : user.username,
                    'profile' : profile_data 
                }, status=200)
            else:
                return JsonResponse({'error' : 'Invalid Username or Password'}, status=400)
            
        except json.JSONDecodeError:
            return JsonResponse({'error' : 'Invalid Json Format'}, status=400)
    
    return JsonResponse({'error' : 'Only POST request are allowed'}, status=405)
        
    
# # List User
@csrf_exempt
def list_user(request):
    if request.method == 'GET':
        users_data = []

        # Get all users
        users = User.objects.all()

        for user in users:
            try:
                profile = UserProfile.objects.get(user=user)

                if profile.is_deleted:
                    continue
                else:
                    profile_data = {
                        'age': profile.age,
                        'email': profile.email,
                        'contact_no': profile.contact_no,
                        'dob': profile.dob
                    }

            except UserProfile.DoesNotExist:
                profile_data = None

            users_data.append({
                'username': user.username,
                'email': user.email,
                'profile': profile_data 
            })
        
        return JsonResponse(users_data, safe=False, status=200)
    
    return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)


# Update or Add UserProfile
@csrf_exempt
def update_user(request):
    if request.method in ['PUT', 'PATCH']:
        try:
            data = json.loads(request.body)
            username = data.get('username')

            try:
                user = User.objects.get(username=username)
            except UserProfile.DoesNotExist:
                return JsonResponse({'error' : 'User doest not exist'})
            
            profile, created = UserProfile.objects.get_or_create(user=user)

            if request.method == 'PUT':
                profile.age = data.get('age', profile.age)
                profile.email = data.get('email', profile.email)
                profile.contact_no = data.get('contact_no', profile.contact_no)
                profile.dob = data.get('dob', profile.dob)
            elif request.method == 'PATCH':
                if 'age' in data:
                    profile.age = data['age']
                if 'email' in data:
                    profile.email = data['email']
                if 'contact_no' in data:
                    profile.contact_no = data['contact_no']
                if 'dob' in data:
                    profile.dob = data['dob']

            profile.save()

            return JsonResponse({
                'message' : 'User Updated Successfully',
                'username' : user.username,
                'profile' : {
                    'age' : profile.age,
                    'email' : profile.email,
                    'contact_no' : profile.contact_no,
                    'dob' : profile.dob
                }
            })

        except json.JSONDecodeError:
            return JsonResponse({'error' : 'Invalid Json Format'}, status=400)
        
    return JsonResponse({'error' : 'Only PUT and PATCH requests are allowed'}, status=405)


@csrf_exempt
def delete_user(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        username = data.get('username')

        try:
            user = User.objects.get(username = username)
            profile = UserProfile.objects.get(user=user)
            profile.is_deleted = True
            profile.save()
            return JsonResponse({'message' : 'User delete successfully'}, status=200)
        
        except UserProfile.DoesNotExist:
            return JsonResponse({'error' : 'User does not exist'}, status=404)

        except UserProfile.DoesNotExist:
            return JsonResponse({'error' : 'User Profile does not exist'}, status=404)
        
    return JsonResponse({'error' : 'Only DELETE request is allowed'}, status=405)



