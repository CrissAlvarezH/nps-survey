from typing import List

from nps.models import Nps
from users.models import User


def nps_create(*, user: User, answer: int) -> Nps:
    return Nps.objects.create(user=user, answer=answer)


def nps_create_bulk(*, nps_surveys: List[Nps]) -> List[Nps]:
    return Nps.objects.bulk_create(nps_surveys)


def nps_list():
    return Nps.objects.all()
