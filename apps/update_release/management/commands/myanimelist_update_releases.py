from django.core.management.base import BaseCommand
from django.conf import settings

from apps.update_release.services.myanimelist.client import Client
from apps.update_release.models import MyAnimeListToken, UpdateRelease
from apps.update_release.choices import UpdateReleaseSources
from apps.update_release.services.myanimelist.exceptions import TokenMissing


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--authorisation_code', type=str, required=False, help='authorisation_code')
        parser.add_argument('--access_token', type=str, required=False, help='access_token')

    def handle(self, *args, **options):
        client = Client(client_id=settings.MYAL_CLIENT_ID,
                        client_secret=settings.MYAL_CLIENT_SECRET)
        access_token = options.get('access_token')
        if authorisation_code := options.get('authorisation_code'):
            token = MyAnimeListToken.objects.order_by('-created').first()
            if not token:
                raise TokenMissing
            code_verifier = token.code_verifier
            response_token = client.generate_new_token(
                authorisation_code=authorisation_code,
                code_verifier=code_verifier,
            )
            token.access_token = response_token['access_token']
            token.refresh_token = response_token['refresh_token']
            token.expires_in = response_token['expires_in']
            token.token_type = response_token['token_type']
            token.save(update_fields=['access_token', 'refresh_token', 'expires_in', 'token_type'])
            access_token = response_token['access_token']

        client.connect(access_token=access_token)
        anime_list = client.search_anime(keyword='naruto')
        for anime in anime_list:
            print(anime)

        UpdateRelease.objects.create(
            source=UpdateReleaseSources.MYANIMELIST,
            content=anime_list
        )
