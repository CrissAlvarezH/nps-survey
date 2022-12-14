# Generated by Django 4.1.2 on 2022-10-27 03:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("nps", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="nps",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="companyuser",
            name="company",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="nps.company"
            ),
        ),
        migrations.AddField(
            model_name="companyuser",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="company",
            name="country_name",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="nps.country"
            ),
        ),
        migrations.AddField(
            model_name="company",
            name="persons",
            field=models.ManyToManyField(
                through="nps.CompanyUser", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
