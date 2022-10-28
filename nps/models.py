from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=150, primary_key=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Company(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=1000, null=True, blank=True)
    country_name = models.ForeignKey("nps.Country", on_delete=models.CASCADE)

    @property
    def total_persons(self) -> int:
        return self.companyuser_set.count()

    def __str__(self) -> str:
        return f"{self.id}: {self.name} ({self.country_name})"


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

    class Meta:
        unique_together = ("company", "user")

    def __str__(self) -> str:
        return f"{self.user} - {self.company}"


class Nps(models.Model):
    answer = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    person = models.ForeignKey(
        "nps.CompanyUser",
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    metadata = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.person.user} -> {self.answer}"
