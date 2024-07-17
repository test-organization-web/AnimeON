from django.core.management import call_command
from django.core.management import BaseCommand
from django.conf import settings
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
            call_command("runserver", '0.0.0.0:8000')
