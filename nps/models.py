# Django
from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=150, primary_key=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Company(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=1000, null=True, blank=True)
    country_name = models.ForeignKey("nps.Country", on_delete=models.CASCADE)
    persons = models.ManyToManyField("users.User", through="nps.CompanyUser")

    def __str__(self) -> str:
        return f"{self.id}: {self.name}"


class CompanyUser(models.Model):

    class Roles(models.TextChoices):
        SHAREHOLDER = "SHAREHOLDER", "Shareholder"
        CONTACT = "CONTACT", "Contact"
        CONSULTANT = "CONSULTANT", "Consultant"
        ACCOUNT_MANAGER = "ACC_MANAGER", "Account manager"

    role = models.CharField(
        max_length=50,
        choices=Roles.choices,
        default=Roles.CONTACT
    )
    company = models.ForeignKey("nps.Company", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)


class Nps(models.Model):
    answer = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user} -> {self.answer}"
