from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RegisterSerializer
from .models import CustomUser, Verification
import random 
from .send_mail import send_otp_mail
from django.utils import timezone
from datetime import timedelta

@api_view(['POST'])
def register_view(request):
    serializer = RegisterSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "success" : "Registration successful.",
            "user" : serializer.data
        })
    return Response(serializer.errors)

@api_view(['POST'])
def forgot_password_view(request):
    email = request.data.get('email')

    if not email:
        return Response({
            "error": "Email is required."
        })
    
    try:
        user = CustomUser.objects.get(email = email)
    except CustomUser.DoesNotExist:
         return Response({
             "error": "User not found."
         })
    
    otp = random.randint(100000, 999999)

    Verification.objects.filter(user = user).delete()
    Verification.objects.create(
        user = user,
        otp = str(otp)
    )

    send_otp_mail(otp, email)

    return Response({
        "success": "OTP sent successful.",
        "email": email
    })

@api_view(['POST'])
def verification_view(request):
    email = request.data.get('email')
    otp = request.data.get('otp')
    
    if not email:
        return Response({
            "error": "Email is required."
        })
    
    if not otp:
        return Response({
            "error": "OTP is required."
        })

    try:
        user = CustomUser.objects.get(email = email)
    except CustomUser.DoesNotExist:
         return Response({
             "error": "User not found."
         })
    
    try:
        verification = Verification.objects.get(
            user=user,
            otp=otp
        )

        verification.delete()

        return Response({
            "success": "Verification successful."
        })
    except Verification.DoesNotExist:
        return Response({
            "error": "Invalid OTP"
        })