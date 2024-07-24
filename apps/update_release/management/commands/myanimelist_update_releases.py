import logging
import time

from urllib.parse import urlparse, parse_qs

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction

from apps.anime.models import Anime
from apps.update_release.services.myanimelist.client import Client
from apps.update_release.models import MyAnimeListToken
from apps.update_release.services.myanimelist.exceptions import TokenMissing, APIException


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--authorisation_code', type=str, required=False, help='authorisation_code')
        parser.add_argument('--access_token', type=str, required=False, help='access_token')

    @transaction.atomic
    def handle(self, *args, **options):
        logger.info('Start commend myanimelist update release', extra={
            'message_id': 'myanimelist_update_release_start',
        })
        client = Client(client_id=settings.MYAL_CLIENT_ID,
                        client_secret=settings.MYAL_CLIENT_SECRET)
        access_token = options.get('access_token')
        if authorisation_code := options.get('authorisation_code'):
            logger.info('Try get new access token by authorisation_code', extra={
                'message_id': 'myanimelist_update_release_get_new_access_token_by_authorisation_code',
                'authorisation_code': authorisation_code,
            })
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
            logger.info('Save new access token', extra={
                'message_id': 'myanimelist_update_release_save_new_access_token',
                'access_token': token.access_token,
                'refresh_token': token.refresh_token,
                'expires_in': token.expires_in,
                'token_type': token.token_type,
            })
            access_token = response_token['access_token']

        client.connect(access_token=access_token)

        parse_suggested_anime = True
        suggested_animes = []
        suggested_anime_kwargs = {'limit': 100}

        while parse_suggested_anime:
            response = client.get_suggested_anime(**suggested_anime_kwargs)
            logger.info('Get response from suggested anime', extra={
                'message_id': 'myanimelist_update_release_get_suggested_anime',
                'response': response
            })
            if 'data' in response:
                suggested_animes.extend(response['data'])
            if 'paging' in response and 'next' in response['paging']:
                url = response['paging']['next']
                parsed_url = urlparse(url)
                query_params = parse_qs(parsed_url.query)
                suggested_anime_kwargs = {
                    'offset': query_params['offset'],
                    'limit': query_params['limit'],
                }
            else:
                parse_suggested_anime = False
            time.sleep(1)

        animes_data = []
        for suggested_anime in suggested_animes:
            logger.info('Get details by anime', extra={
                'message_id': 'myanimelist_update_release_get_detail_anime',
                'data': suggested_anime
            })
            try:
                response = client.get_anime_details(id=suggested_anime['node']['id'])
            except APIException as error:
                logger.exception(error)
                if error.status_code == 503:
                    time.sleep(60)
                    response = client.get_anime_details(id=suggested_anime['node']['id'])
                else:
                    raise
            except Exception as error:
                logger.exception(error)
                raise
            logger.info('Get response by anime', extra={
                'message_id': 'myanimelist_update_release_get_response_anime',
                'response': response
            })
            anime_data = Anime(
                title=response.get('title'),
                type=response.get('media_type'),
                start_date=response.get('start_date'),
                end_date=response.get('end_date'),
                status=response.get('status'),
                rating=response.get('rating'),
                description=response.get('synopsis'),
                short_description=response.get('synopsis'),
                season=response.get('start_season', {}).get('season'),
                year=response.get('start_season', {}).get('year'),
            )
            animes_data.append(anime_data)
            logger.info('Finish parse anime', extra={
                'message_id': 'myanimelist_update_release_finish_parse_anime',
                'data': suggested_anime
            })
            time.sleep(1)

        logger.info('Start bulk create animes', extra={
            'message_id': 'myanimelist_update_release_start_bulk_create',
            'count_anime': len(animes_data)
        })

        Anime.objects.bulk_create(animes_data, batch_size=1000)

        logger.info('Finish bulk create animes', extra={
            'message_id': 'myanimelist_update_release_finish_bulk_create',
            'count_anime': len(animes_data)
        })

        logger.info('Finish commend myanimelist update release', extra={
            'message_id': 'myanimelist_update_release_finish',
        })
