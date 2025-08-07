from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from . import serializers
from . import models
import random

class RegistrationViewSet(APIView):
    def get(self, request):
        return Response({
            "message" : "Registration(GET)"
        })
    
    def post(self, request):
        serializer = serializers.RegistrationSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success" : "Registration successful."
            })
        return Response(serializer.errors)
    
class LoginViewSet(APIView):
    def get(self, request):
        return Response({
            "message" : "Login(GET)"
        })
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email:
            return Response({
                "error" : "Email is required."
            })
        
        if not password:
            return Response({
                "error" : "Password is required."
            })
        
        user = authenticate(email = email, password = password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "success" : "Login successful",
                "refresh" : str(refresh),
                "access" : str(refresh.access_token),
            })
        
        if models.CustomUser.objects.filter(email=email).exists():
            return Response({
                "error" : "Password does not match."
            })
        else:
            return Response({
                "error" : "User does not exist."
            })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({
        "message" : "It's a protected view."
    })
        
class RefreshView(APIView):
    def post(self, request):
        refresh = request.data.get('refresh')

        if not refresh:
            return Response({
                "error" : "Refresh token required."
            })
        
        token = RefreshToken(refresh)
        return Response({
            'access' : str(token.access_token)
        })
    
class ForgotPasswordViewSet(APIView):
    def get(self, request):
        return Response({
            "message" : "Forgot password(GET)"
        })
    
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({
                "error" : "Email is required."
            })
        
        try:
            user = models.CustomUser.objects.get(email = email)
            models.Verification.objects.filter(user = user).delete()
            otp = random.randint(10000000, 99999999)
            models.Verification.objects.create(
                user = user,
                otp = otp
            )
            return Response(
                {
                    "success" : "OTP sent successfully.",
                    "email" : email
                }
            )
        
        except models.CustomUser.DoesNotExist:
            return Response({
                "error" : "User does not exist."
            })
        
class VerificationViewSet(APIView):
    def get(self, request):
        return Response({
            "message" : "Verification(GET)"
        })
    
    def post(self, request):
        email = request.data.get('email')
        up_otp = request.data.get('otp')

        if not email:
            return Response({
                "error" : "Email is required."
            })

        if not up_otp:
            return Response({
                "error" : "OTP is required."
            })
        
        try: 
            user = models.CustomUser.objects.get(email = email)
            verification = models.Verification.objects.get(user = user)

            if str(up_otp) == str(verification.otp):
                verification.delete()
                return Response({
                    "success" : "Verification successful",
                    "email" : email
                })
            return Response({
                "error" : "Verification failed."
            })
        
        except models.CustomUser.DoesNotExist:
            return Response({
                "error" : "User does not exist."
            })
        
        except models.Verification.DoesNotExist:
            return Response({
                "error" : "OTP not found."
            })
        
class PasswordResetViewSet(APIView):
    def get(self, request):
        return Response({
            "message" : "Password reset(GET)"
        })
    
    def post(self, request):
        serializer = serializers.PasswordResetSerializer(data = request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password_1']

            try: 
                user = models.CustomUser.objects.get(email = email)
                user.set_password(password)
                user.save()
                return Response({
                    "success" : "Password reset successful."
                })

            except models.CustomUser.DoesNotExist:
                return Response({
                    "error" : "User does not exist."
                })
            
        return Response(serializer.errors)