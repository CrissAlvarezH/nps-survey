# Django
from django.db import models
from django.contrib.auth.models import AbstractUser

from nps.models import Company, CompanyUser


class User(AbstractUser):
    full_name = models.CharField(max_length=500)
    username = models.CharField(max_length=100, blank=True, null=True)  # Not is necessary
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

    @property
    def companies(self):
        relationship = CompanyUser.objects.filter(user_id=self.id)
        return [r.company for r in relationship]

    def __str__(self) -> str:
        return f"{self.id}: {self.email}"
