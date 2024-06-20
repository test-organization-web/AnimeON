from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.management import call_command

from apps.update_release.services.myanimelist.client import Client
from apps.update_release.models import MyAnimeListToken


class Command(BaseCommand):

    def handle(self, *args, **options):
        client = Client(client_id=settings.MYAL_CLIENT_ID, client_secret=settings.MYAL_CLIENT_SECRET)
        active_token = MyAnimeListToken.objects.get_active()
        if active_token:
            call_command('myanimelist_update_releases', access_token=active_token.access_token)
        else:
            code_verifier = code_challenge = client.get_new_code_verifier()
            authorisation_url = client.new_authorisation_url(code_challenge=code_challenge)
            MyAnimeListToken.objects.create(
                code_verifier=code_verifier,
                code_challenge=code_challenge,
                authorisation_url=authorisation_url,
            )
