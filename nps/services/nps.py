from typing import List, Optional

from nps.models import CompanyUser, Nps
from users.models import User


def nps_create(
    *,
    user: Optional[User] = None,
    company_id: Optional[int] = None,
    answer: int
) -> Nps:
    person = CompanyUser.objects.get(user_id=user.id, company_id=company_id)
    return Nps.objects.create(person=person, answer=answer)


def nps_create_bulk(*, nps_surveys: List[Nps]) -> List[Nps]:
    return Nps.objects.bulk_create(nps_surveys)


def nps_list(**filters):
    if filters:
        return Nps.objects.filter(**filters)
    else:
        return Nps.objects.all()
