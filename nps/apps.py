from django.apps import AppConfig


class NpsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nps'

    def ready(self) -> None:
        from nps import receivers
        return super().ready()
