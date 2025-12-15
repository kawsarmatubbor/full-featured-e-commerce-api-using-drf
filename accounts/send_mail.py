from django.core.mail import send_mail
from django.conf import settings

def send_otp_mail(otp, email):
    send_mail(
        subject='Verification OTP',
        message=f'Your verification OTP is {otp}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )

