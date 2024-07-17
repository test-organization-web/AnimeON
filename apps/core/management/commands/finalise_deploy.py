from django.core.management import call_command
from django.core.management import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model
import subprocess
import traceback
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        errors = []
        try:
            # static files
            call_command("collectstatic", interactive=False)
            # migrate and save migrations state
            call_command("migrate", interactive=False)
        except subprocess.CalledProcessError as e:
            errors.append(e.stderr.decode())
            errors.append(traceback.format_exc())
            raise
        except Exception:
            errors.append(traceback.format_exc())
            raise
        else:
            admin_username = settings.ADMIN_USERNAME
            admin_password = settings.ADMIN_PASSWORD
            call_command("runserver", '0.0.0.0:8000')
            if get_user_model().objects.filter(username=admin_username).exists():
                logger.warning('Superuser exists already')
            else:
                get_user_model().objects.create_superuser(admin_username,
                                                          password=admin_password)
                logger.info('Superuser was created successfully')
