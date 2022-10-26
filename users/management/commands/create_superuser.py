# Django
import logging
from django.core.management.base import BaseCommand
# Local
from config.settings import SUPER_USER_EMAIL, SUPER_USER_PASSWORD
# This app
from users.services import user_create, user_exists


LOG = logging.getLogger("users-commands")


class Command(BaseCommand):

    def handle(self, *args, **options):
        if user_exists(email=SUPER_USER_EMAIL):
            LOG.warning("superuser already exists")
            return

        user_create(
            name="Root",
            email=SUPER_USER_EMAIL,
            password=SUPER_USER_PASSWORD,
            is_superuser=True
        )
        LOG.info("superuser created")
