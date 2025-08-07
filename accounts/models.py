from django.db import models
from django.contrib.auth.models import AbstractUser
from . import manager

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=254, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = manager.CustomUserManager()

    def __str__(self):
        return self.email
    
class Verification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp = models.IntegerField()