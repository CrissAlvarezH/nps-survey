# Django
import logging
from django.core.management.base import BaseCommand

from nps.services import country_create, country_exists
# This app


LOG = logging.getLogger("nps-commands")


COUNTRIES = [
    "Argentina", "Bolivia", "Brasil", "Chile", "Colombia", "Costa Rica",
    "Cuba", "Ecuador"
]


class Command(BaseCommand):

    def handle(self, *args, **options):
        for country in COUNTRIES:
            if not country_exists(name=country):
                country_create(name=country)
