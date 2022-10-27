from typing import List

from .models import User


def user_create(
    *, name: str, email: str, password: str, is_superuser: bool = False
) -> User:
    user = User.objects.create(
        full_name=name,
        email=email
    )
    user.set_password(password)
    if is_superuser:
        user.is_superuser = True
        user.is_staff = True
    user.save()
    return user


def user_exists(*, email: str) -> bool:
    return User.objects.filter(email=email).exists()


def user_bulk_create(*, users: List[User]):
    return User.objects.bulk_create(users)
