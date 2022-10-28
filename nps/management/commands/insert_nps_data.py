import random
import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password

from faker import Faker
from faker.providers import company as company_faker, profile as profile_faker

from nps.models import Company, CompanyUser, Nps
from nps.services.companies import add_person_to_company_bulk, company_bulk_create
from nps.services.countries import country_get
from nps.services.nps import nps_create_bulk, nps_list
from users.services import user_bulk_create, user_exists
from users.models import User

from .insert_countries import COUNTRIES


LOG = logging.getLogger("nps-commands")


class Command(BaseCommand):

    def handle(self, *args, **options):
        if nps_list().exists():
            return "nps data is already inserted"

        faker = Faker()
        faker.add_provider(company_faker)
        faker.add_provider(profile_faker)

        LOG.info("start to insert companies")
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

        LOG.info("start to insert people")
        # create 8 people for each company
        people = []
        amount_of_people = len(companies_in_db) * 8
        for _ in range(amount_of_people):
            profile = faker.profile(["name", "mail"])
            if user_exists(email=profile["mail"]):
                continue

            user = User(
                full_name=profile["name"],
                email=profile["mail"],
                password=make_password("123456"),
            )
            people.append(user)

        users_in_db = user_bulk_create(users=people)

        LOG.info("start to insert user company relationship")
        # add 8 people to each company
        roles = [c[0] for c in CompanyUser.Roles.choices]
        company_user_relationships = []
        offset = 0
        for company in companies_in_db:
            users = users_in_db[offset:offset + 8]
            for user in users:
                company_user = CompanyUser(
                    user=user,
                    company=company,
                    role=random.choice(roles)
                )
                company_user_relationships.append(company_user)

            offset = offset + 8

        company_users_in_db = add_person_to_company_bulk(
            relationships=company_user_relationships)

        LOG.info("start to insert nps surveys")
        # insert nps surveys
        nps_surveys = []
        for person in company_users_in_db:
            nps_answer = Nps(person=person, answer=random.randint(0, 10))
            nps_surveys.append(nps_answer)

        nps_create_bulk(nps_surveys=nps_surveys)

        return "nps data inserted successfully"
