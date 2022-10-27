from typing import Optional, List

from nps.models import Company, CompanyUser
from nps.services.countries import country_get
from users.services import user_get


def company_exist(*, name: str) -> bool:
    return Company.objects.filter(name=name).exists()


def company_exist_by_id(*, id: int) -> bool:
    return Company.objects.filter(id=id).exists()


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


def company_get(id: int) -> Company:
    return Company.objects.get(id=id)


def company_bulk_create(*, companies: List[Company]):
    return Company.objects.bulk_create(companies)


def add_person_to_company(*, user_id: int, company_id: int, role: str):
    return CompanyUser.objects.create(
        role=role,
        user=user_get(id=user_id),
        company=company_get(id=company_id)
    )


def update_person_rol(*, user_id: str, company_id: int, role: str) -> CompanyUser:
    person = CompanyUser.objects.get(user_id=user_id, company_id=company_id)
    person.role = role
    person.save()
    return person


def person_company_relationship_exists(*, user_id: int, company_id: int) -> bool:
    return CompanyUser.objects.filter(
        user_id=user_id, company_id=company_id
    ).exists()


def add_person_to_company_bulk(*, relationships: List[CompanyUser]):
    return CompanyUser.objects.bulk_create(relationships)


def remove_person_from_company(*, company_id: int, user_id: int):
    CompanyUser.objects.filter(
        company_id=company_id, user_id=user_id
    ).delete()
