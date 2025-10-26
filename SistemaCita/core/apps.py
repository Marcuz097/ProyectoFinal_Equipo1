from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Importar aquí para que Django ya haya cargado el ORM
        from .utils import crear_admin
        crear_admin()