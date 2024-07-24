import logging
import secrets

from typing import Optional
from apps.update_release.services.myanimelist.request_handler import APICaller
from apps.update_release.services.myanimelist.anime import AnimeMixin
from apps.update_release.models import MyAnimeListToken

logger = logging.getLogger(__name__)


class Client(AnimeMixin):
    """
    MAL Base Client Object for interfacing with the MAL REST API.
    """

    def __init__(self, client_id, client_secret):
        self.anime_fields = [
            "id",
            "title",
            "main_picture",
            "alternative_titles",
            "start_date",
            "end_date",
            "synopsis",
            "mean",
            "rank",
            "popularity",
            "num_list_users",
            "num_scoring_users",
            "nsfw",
            "created_at",
            "updated_at",
            "media_type",
            "status",
            "genres",
            "my_list_status",
            "num_episodes",
            "start_season",
            "broadcast",
            "source",
            "average_episode_duration"
            "rating",
            "pictures",
            "background",
            "related_anime",
            "related_manga",
            "recommendations",
            "studios",
            "statistic",
        ]

        self.manga_fields = [
            "id",
            "title",
            "main_picture",
            "alternative_titles",
            "start_date",
            "end_date",
            "synopsis",
            "mean",
            "rank",
            "popularity",
            "num_list_users",
            "num_scoring_users",
            "nsfw,created_at",
            "updated_at",
            "media_type,status",
            "genres",
            "my_list_status",
            "num_volumes",
            "num_chapters",
            "authors{first_name,last_name}",
            "pictures",
            "background",
            "related_anime",
            "related_manga",
            "recommendation",
        ]
        self.client_id = client_id
        self.client_secret = client_secret

    # 1. Generate a new Code Verifier / Code Challenge.
    @staticmethod
    def get_new_code_verifier() -> str:
        token = secrets.token_urlsafe(100)
        return token[:128]

    # 2. Print the URL needed to authorise your application.
    def new_authorisation_url(self, code_challenge: str, state: str = ''):
        base_url = 'https://myanimelist.net/v1'
        uri = 'oauth2/authorize'
        return f'{base_url}/{uri}?state={state}&response_type=code&client_id={self.client_id}&code_challenge={code_challenge}'

    # 3. Once you've authorised your application, you will be redirected to the webpage you've
    #    specified in the API panel. The URL will contain a parameter named "code" (the Authorisation
    #    Code). You need to feed that code to the application.
    def generate_new_token(self, authorisation_code: str, code_verifier: str) -> dict:
        base_url = 'https://myanimelist.net/v1/'
        uri = 'oauth2/token'
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': authorisation_code,
            'code_verifier': code_verifier,
            'grant_type': 'authorization_code'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        api_handler = APICaller(base_url=base_url, headers=headers)
        logger.info('Generate new myanimelist token', extra={
            'message_id': 'myanimelist_client_generate_new_token',
        })
        return api_handler.call(uri=uri, method="post", data=data)

    def connect(self, access_token: Optional[str] = None, refresh_token: Optional[str] = None):
        base_url = "https://api.myanimelist.net/"
        version = 'v2'
        self.base_url = base_url + f'{version}/'
        self.bearer_token = access_token
        self.refresh_token = refresh_token
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Bearer {self.bearer_token}'
        }
        logger.info('Connect to myanimelist with params', extra={
            'message_id': 'myanimelist_connect_prepare_params',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'base_url': self.base_url,
        })
        self._api_handler = APICaller(base_url=self.base_url,
                                      headers=self.headers)

    def refresh_bearer_token(self, refresh_token, client_secret=None):
        base_url = "https://myanimelist.net/v1/"
        uri = "oauth2/token"
        headers = {
            'Authorization': f'Bearer {self.bearer_token}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        api_handler = APICaller(base_url=base_url, headers=headers)
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.client_id
        }

        if client_secret:
            data["client_secret"] = client_secret

        # print response json of authentication, reinstantiate caller method.
        logger.info('Refresh myanimelist bearer token', extra={
            'message_id': 'myanimelist_client_refresh_bearer_token',
        })
        response = api_handler.call(uri=uri, method="post", data=data)
        logger.info(f"Refreshing token with client id and secret: {response}")
        self.bearer_token = response.access_token
        self.refresh_token = response.refresh_token
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Bearer {response.access_token}',
            'X-MAL-Client-ID': '{}'
        }
        logger.info('Connect to myanimelist with params', extra={
            'message_id': 'myanimelist_connect_prepare_params',
            'bearer_token': self.bearer_token,
            'refresh_token': self.refresh_token,
            'base_url': self.base_url,
        })
        self._api_handler = APICaller(base_url=self.base_url,
                                      headers=self.headers)
        return

    def auth(self) -> dict:
        logger.info('Start auth into Myanimelist', extra={
            'message_id': 'myanimelist_auth_start'
        })
        active_token = MyAnimeListToken.objects.get_active()
        if active_token:
            logger.info('Myanimelist has active token', extra={
                'message_id': 'myanimelist_auth_has_active_token',
                'access_token': active_token.access_token,
                'active_token_id': active_token.id
            })
            return {'type': 'token', 'token': active_token.access_token}
        logger.info('Start get auth token myanimelist', extra={
            'message_id': 'myanimelist_auth_get_auth_token',
        })
        code_verifier = code_challenge = self.get_new_code_verifier()
        authorisation_url = self.new_authorisation_url(code_challenge=code_challenge)
        logger.info('Get auth url Myanimelist', extra={
            'message_id': 'myanimelist_auth_get_auth_url',
            'authorisation_url': authorisation_url,
            'code_verifier': code_verifier,
            'code_challenge': code_challenge,
        })
        MyAnimeListToken.objects.create(
            code_verifier=code_verifier,
            code_challenge=code_challenge,
            authorisation_url=authorisation_url,
        )
        logger.info('Finish auth into Myanimelist', extra={
            'message_id': 'myanimelist_auth_finish',
        })
        return {'type': 'url', 'url': authorisation_url}
