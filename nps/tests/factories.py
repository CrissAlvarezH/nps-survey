from faker import Faker
from faker.providers import company as company_faker, profile as profile_faker
from nps.models import Company, Country

from users.models import User


faker = Faker()
faker.add_provider(company_faker)
faker.add_provider(profile_faker)


class UserFactory:
    @classmethod
    def create(cls, amount: int = 1):
        users = []
        for _ in range(amount):
            profile = faker.profile(["name", "mail"])
            users.append(User(
                full_name=profile["name"],
                email=profile["mail"]
            ))

        result = User.objects.bulk_create(users)
        return result[0] if amount == 1 else result


class CountryFactory:
    @classmethod
    def create(cls, amount: int = 1):
        countries = []
        for _ in range(amount):
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
