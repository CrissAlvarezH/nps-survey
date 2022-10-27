from nps.models import Country


def country_create(*, name: str) -> Country:
    return Country.objects.create(name=name)


def country_get(*, name: str) -> Country:
    return Country.objects.get(name=name)


def country_exists(*, name: str) -> bool:
    return Country.objects.filter(name=name).exists()
