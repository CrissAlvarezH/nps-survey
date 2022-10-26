# Django
from django.db import models
from django.contrib.auth.models import AbstractUser


class Profile(models.Model):
    """ Profile data of one user

    Holds the data associated to business logic
    """
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)


class User(AbstractUser):
    full_name = models.CharField(max_length=500)
    username = models.CharField(max_length=100, blank=True, null=True)  # Not is necessary
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']
