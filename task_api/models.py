from django.db import models
from django.contrib.auth.models import AbstractUser


# Create models
class User(AbstractUser):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
