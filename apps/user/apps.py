from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.user.signals import create_auth_token
from django.conf import settings


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.user'


    def ready(self):
        post_save.connect(create_auth_token, sender=settings.AUTH_USER_MODEL)
