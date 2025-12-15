from django.urls import path
from .views import register_view, forgot_password_view, verification_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('forgot-password/', forgot_password_view, name='forgot_password'),
    path('verification/', verification_view, name='verification'),
]
