from typing import Optional, List

from nps.models import Company, CompanyUser
from nps.services.countries import country_get
from users.models import User


def company_exist(*, name: str) -> bool:
    return Company.objects.filter(name=name).exists()


def company_create(
    *,
    name: str,
    country: str,
    description: Optional[str] = None,
) -> Company:
    return Company.objects.create(
        name=name,
        description=description,
        country_name=country_get(name=country)
    )


def company_list():
    return Company.objects.all()


def company_bulk_create(*, companies: List[Company]):
    return Company.objects.bulk_create(companies)


def add_person_to_company(user: User, company: Company, role: str):
    CompanyUser.objects.create(
        role=role,
        user=user,
        company=company
    )


def add_person_to_company_bulk(relationships: List[CompanyUser]):
    return CompanyUser.objects.bulk_create(relationships)
