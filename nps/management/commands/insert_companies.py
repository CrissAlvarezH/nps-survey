import random
import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password

from faker import Faker
from faker.providers import company as company_faker, profile as profile_faker

from nps.models import Company, CompanyUser
from nps.services import company_exist
from nps.services.companies import add_person_to_company_bulk, company_bulk_create
from nps.services.countries import country_get
from users.services import user_bulk_create, user_exists
from users.models import User

from .insert_countries import COUNTRIES


LOG = logging.getLogger("nps-commands")


class Command(BaseCommand):

    def handle(self, *args, **options):
        faker = Faker()
        faker.add_provider(company_faker)
        faker.add_provider(profile_faker)

        companies = []
        for country in COUNTRIES:
            # create companies by country
            for _ in range(random.randint(3, 5)):
                company_name = faker.company()
                company = Company(
                    name=company_name,
                    description=faker.catch_phrase(),
                    country_name=country_get(name=country)
                )
                companies.append(company)

        companies_in_db = company_bulk_create(companies=companies)

        # create 5 people for each company
        people = []
        amount_of_people = len(companies_in_db) * 5
        for _ in range(amount_of_people):
            profile = faker.profile(["name", "mail"])
            user = User(
                full_name=profile["name"],
                email=profile["mail"],
                password=make_password("123456"),
            )
            people.append(user)

        users_in_db = user_bulk_create(users=people)

        # add 10 people to each company
        roles = [c[0] for c in CompanyUser.Roles.choices]
        company_user_relationships = []
        for index, company in enumerate(companies_in_db):
            users = users_in_db[index:index + 10]
            for user in users:
                company_user = CompanyUser(
                    user=user,
                    company=company,
                    role=random.choice(roles)
                )
                company_user_relationships.append(company_user)

        add_person_to_company_bulk(company_user_relationships)
