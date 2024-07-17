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
            subprocess.run(
                [
                    'aws', 's3', 'sync',
                    settings.STATIC_ROOT,
                    f's3://{settings.AWS_STORAGE_BUCKET_NAME}/static',
                    '--acl', 'public-read',
                ],
                check=True,
                capture_output=True
            )
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
