from django.apps import AppConfig


class AppClienteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_cliente'

    def ready(self):
        import app_cliente.signals