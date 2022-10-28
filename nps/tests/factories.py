import email
import random

from faker import Faker
from faker.providers import company as company_faker, profile as profile_faker
from nps.models import Company, CompanyUser, Country

from users.models import User


faker = Faker()
faker.add_provider(company_faker)
faker.add_provider(profile_faker)


class UserFactory:
    @classmethod
    def create(cls, amount: int = 1):
        users = []
        while len(users) < amount:
            profile = faker.profile(["name", "mail"])

            # avoid duplicity
            if profile["mail"] in [u.email for u in users]:
                continue
            if User.objects.filter(email=profile["mail"]).exists():
                continue

            users.append(User(
                full_name=profile["name"],
                email=profile["mail"]
            ))

        result = User.objects.bulk_create(users)
        return result[0] if amount == 1 else result

    @classmethod
    def create_company_relationship(cls, company: Company, amount: int = 1):
        roles = [r[0] for r in CompanyUser.Roles.choices]

        relationships = []
        for _ in range(amount):
            relationships.append(CompanyUser(
                user=cls.create(),
                company=company,
                role=random.choice(roles)
            ))

        return CompanyUser.objects.bulk_create(relationships)


class CountryFactory:
    @classmethod
    def create(cls, amount: int = 1):
        countries = []
        while len(countries) < amount:
            name = faker.company()
            if name in [c.name for c in countries]:
                continue  # avoid duplicity
            countries.append(Country(name=faker.country()))

        result = Country.objects.bulk_create(countries)
        return result[0] if amount == 1 else result


class CompanyFactory:
    @classmethod
    def create(cls, country: Country, amount: int = 1):
        companies = []
        while len(companies) < amount:
            company_name = faker.company()
            if company_name in [c.name for c in companies]:
                continue  # avoid duplicity

            companies.append(Company(
                name=faker.company(),
                description=faker.catch_phrase(),
                country_name=country
            ))

        result = Company.objects.bulk_create(companies)
        return result[0] if amount == 1 else result
