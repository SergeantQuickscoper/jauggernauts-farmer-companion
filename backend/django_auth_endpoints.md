
## Models

### FarmerProfile Model
Add this to your `models.py`:

```python
from django.db import models
from django.contrib.auth.models import User

class FarmerProfile(models.Model):
    """Extended profile for farmers"""
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='farmer_profile'
    )
    district = models.CharField(max_length=100)
    farm_area = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Farm area in hectares"
    )
    crops = models.JSONField(
        default=list,
        help_text="Array of crop names grown by the farmer"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'farmer_profiles'
        verbose_name = 'Farmer Profile'
        verbose_name_plural = 'Farmer Profiles'
    
    def __str__(self):
        return f"{self.user.username} - {self.district}"
    
    @property
    def farm_area_display(self):
        return f"{self.farm_area} hectares"
    
    @property
    def crops_display(self):
        return ", ".join(self.crops) if self.crops else "No crops specified"
```

## Serializers

Add these to your `serializers.py`:

```python
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
import re

class FarmerProfileSerializer(serializers.ModelSerializer):
    """Serializer for FarmerProfile model"""
    
    class Meta:
        model = FarmerProfile
        fields = ['district', 'farm_area', 'crops']
    
    def validate_farm_area(self, value):
        if value <= 0:
            raise serializers.ValidationError("Farm area must be greater than 0")
        return value
    
    def validate_crops(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Crops must be an array/list")
        if len(value) == 0:
            raise serializers.ValidationError("At least one crop must be specified")
        
        cleaned_crops = []
        for crop in value:
            if isinstance(crop, str) and crop.strip():
                cleaned_crops.append(crop.strip().title())
        
        if not cleaned_crops:
            raise serializers.ValidationError("At least one valid crop name must be provided")
        
        return cleaned_crops


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    # Farmer profile fields
    district = serializers.CharField(max_length=100)
    farm_area = serializers.DecimalField(max_digits=10, decimal_places=2)
    crops = serializers.ListField(
        child=serializers.CharField(max_length=50),
        min_length=1
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 
                 'first_name', 'last_name', 'district', 'farm_area', 'crops']
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists")
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, value):
            raise serializers.ValidationError("Invalid email format")
        
        return value
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        
        try:
            validate_password(data['password'])
        except ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})
        
        if data['farm_area'] <= 0:
            raise serializers.ValidationError("Farm area must be greater than 0")
        
        if not data['crops'] or len(data['crops']) == 0:
            raise serializers.ValidationError("At least one crop must be specified")
        
        return data
    
    def create(self, validated_data):
      
        district = validated_data.pop('district')
        farm_area = validated_data.pop('farm_area')
        crops = validated_data.pop('crops')
        validated_data.pop('password_confirm')
        
  
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
      
        FarmerProfile.objects.create(
            user=user,
            district=district,
            farm_area=farm_area,
            crops=crops
        )
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required")
        return value
    
    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("Password is required")
        return value
```

## Views

Create or update your `views.py`:

```python
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.db import transaction
from .models import FinanceAccount, FarmerProfile
from .serializers import UserRegistrationSerializer, UserLoginSerializer, FarmerProfileSerializer

class UserRegistrationView(APIView):
    """User registration endpoint for farmers"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = serializer.save()
                    token, created = Token.objects.get_or_create(user=user)
                    
                  
                    FinanceAccount.objects.create(
                        farmer=user,
                        account_name="Default Cash Account",
                        account_type="CASH",
                        current_balance=0.00
                    )
                    
                    return Response({
                        'message': 'User registered successfully',
                        'user_id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'token': token.key,
                        'farmer_profile': {
                            'district': user.farmer_profile.district,
                            'farm_area': float(user.farmer_profile.farm_area),
                            'crops': user.farmer_profile.crops
                        }
                    }, status=status.HTTP_201_CREATED)
                    
            except Exception as e:
                return Response({
                    'error': 'Registration failed',
                    'details': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """User login endpoint"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            try:
                user = User.objects.get(email=email)
                authenticated_user = authenticate(
                    request=request,
                    username=user.username,
                    password=password
                )
                
                if authenticated_user:
                    token, created = Token.objects.get_or_create(user=authenticated_user)
                    
                    return Response({
                        'message': 'Login successful',
                        'user_id': authenticated_user.id,
                        'username': authenticated_user.username,
                        'email': authenticated_user.email,
                        'token': token.key,
                        'farmer_profile': {
                            'district': authenticated_user.farmer_profile.district,
                            'farm_area': float(authenticated_user.farmer_profile.farm_area),
                            'crops': authenticated_user.farmer_profile.crops
                        }
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'error': 'Invalid credentials'
                    }, status=status.HTTP_401_UNAUTHORIZED)
                    
            except User.DoesNotExist:
                return Response({
                    'error': 'User with this email does not exist'
                }, status=status.HTTP_404_NOT_FOUND)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """User logout endpoint"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                'error': 'Logout failed'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """Get and update user profile"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        return Response({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'farmer_profile': {
                'district': user.farmer_profile.district,
                'farm_area': float(user.farmer_profile.farm_area),
                'crops': user.farmer_profile.crops
            }
        }, status=status.HTTP_200_OK)
    
    def put(self, request):
        serializer = FarmerProfileSerializer(
            instance=request.user.farmer_profile,
            data=request.data,
            partial=True
        )
        
        if serializer.is_valid():
            serializer.save()
            
            user = request.user
            if 'first_name' in request.data:
                user.first_name = request.data['first_name']
            if 'last_name' in request.data:
                user.last_name = request.data['last_name']
            user.save()
            
            return Response({
                'message': 'Profile updated successfully',
                'farmer_profile': {
                    'district': user.farmer_profile.district,
                    'farm_area': float(user.farmer_profile.farm_area),
                    'crops': user.farmer_profile.crops
                }
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

## URLs

Update your `urls.py`:

```python
from django.urls import path
from .views import (
    UserRegistrationView, UserLoginView, LogoutView, UserProfileView,
    # Add  existing views here
)

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', UserRegistrationView.as_view(), name='user-register'),
    path('auth/login/', UserLoginView.as_view(), name='user-login'),
    path('auth/logout/', LogoutView.as_view(), name='user-logout'),
    path('auth/profile/', UserProfileView.as_view(), name='user-profile'),
    
    # Add  existing URL patterns here
]
```

## Setup Instructions

1. **Update settings.py**:
```python
INSTALLED_APPS = [
    # ... existing apps
    'rest_framework',
    'rest_framework.authtoken',  # Add this
    'corsheaders',
    # ... your apps
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

2. **Run migrations**:
```bash
python manage.py makemigrations
python manage.py migrate
```

## API Examples

### User Registration
```http
POST /api/auth/register/
Content-Type: application/json

{
    "username": "farmer123",
    "email": "farmer123@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "first_name": "abhinav",
    "last_name": "challa",
    "district": "Punjab",
    "farm_area": 5.5,
    "crops": ["wheat", "rice", "corn"]
}
```

### User Login
```http
POST /api/auth/login/
Content-Type: application/json

{
    "email": "farmer123@example.com",
    "password": "SecurePass123!"
}
```

### Get Profile
```http
GET /api/auth/profile/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

### Update Profile
```http
PUT /api/auth/profile/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
Content-Type: application/json

{
    "district": "Haryana",
    "farm_area": 7.2,
    "crops": ["wheat", "sugarcane", "mustard"]
}
```

### Logout
```http
POST /api/auth/logout/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

## Available Endpoints

- **POST /api/auth/register/** - User registration with farmer profile
- **POST /api/auth/login/** - User login (email/password)
- **GET /api/auth/profile/** - Get user profile
- **PUT /api/auth/profile/** - Update user profile
- **POST /api/auth/logout/** - User logout

All protected endpoints require the Authorization header:
```
Authorization: Token <abhinav_challa>
```