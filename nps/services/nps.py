from typing import List, Optional

from nps.models import CompanyUser, Nps
from users.models import User


def nps_create(
    *,
    user: Optional[User] = None,
    company_id: Optional[int] = None,
    metadata: Optional[dict] = None,
    answer: int
) -> Nps:
    person = CompanyUser.objects.get(user_id=user.id, company_id=company_id)
    return Nps.objects.create(person=person, answer=answer, metadata=metadata)


def nps_create_bulk(*, nps_surveys: List[Nps]) -> List[Nps]:
    return Nps.objects.bulk_create(nps_surveys)


def nps_get_by_id(id: int) -> Nps:
    return Nps.objects.get(id=id)


def nps_update(*, id: int, **kwargs) -> Nps:
    nps = nps_get_by_id(id)
    for key, value in kwargs.items():
        nps.__setattr__(key, value)
    nps.save()
    return nps


def nps_list(**filters):
    if filters:
        return Nps.objects.filter(**filters)
    else:
        return Nps.objects.all()
