from django.apps import AppConfig


class PollsConfig(AppConfig):
    """
        Configuration class for the 'polls' application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
