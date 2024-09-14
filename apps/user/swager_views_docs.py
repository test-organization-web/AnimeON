from drf_yasg import openapi
from rest_framework import status

from apps.core.swagger_views_docs import BaseSwaggerAPIViewDoc, SwaggerTags
from apps.core.serializers import ResponseErrorSerializer
from apps.user.serializers import UserSerializer, ResponsePaginatedUserAnimeListSerializer


class UserAPIViewDoc(BaseSwaggerAPIViewDoc):
    """
    It is a Swagger doc for 'UserAPIView'
    """
    tags = [SwaggerTags.USER]

    responses = {
        status.HTTP_200_OK: openapi.Response(
            'Ok.',
            UserSerializer,
            examples={'application/json': {
                'username': 'test',
                'count_viewed_anime': '5',
                'count_commented_anime': '5',
            }},
        ),
    }


class UserAnimeListAPIViewDoc(BaseSwaggerAPIViewDoc):
    """
    It is a Swagger doc for 'UserAnimeListAPIView'
    """
    tags = [SwaggerTags.USER]

    parameters = [
        openapi.Parameter(
            'action',
            openapi.IN_QUERY,
            description="Filter by action (FAVORITE, VIEWED, DROPPED, PLANNED, WATCHING)",
            type=openapi.TYPE_STRING
        ),
    ]

    responses = {
        status.HTTP_200_OK: openapi.Response(
            'Ok.',
            ResponsePaginatedUserAnimeListSerializer,
            examples={
                'application/json': {
                    "active_page": 1,
                    "num_pages": 1,
                    "count": 1,
                    "next": "<str: url>",
                    "previous": "<str: url>",
                    "results": [
                        {
                            'action': 'FAVORITE',
                            'anime': {
                                'id': 1,
                                'title': 'Naruto',
                                'card_image': '/path/to/naruto/image.jpg',
                                'count_episodes': 5,
                                'slug': 'naruto',
                                'type': 'TV',
                                'year': 2012,
                            }
                        }, {
                            'action': 'FAVORITE',
                            'anime': {
                                'id': 2,
                                'title': 'One Piece',
                                'card_image': '/path/to/onepiece/image.jpg',
                                'count_episodes': 3,
                                'slug': 'one-piece',
                                'type': 'TV',
                                'year': 2012,
                            }
                        }
                    ]
                }
            },
        ),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(
            'Unauthorized.',
            examples={
                'application/json': {
                    "errors": [
                        {
                            "message": "Реквізити перевірки достовірності не надані.",
                        },
                    ]
                }
            },
        ),
    }


class UserAnimeAPIViewDoc(BaseSwaggerAPIViewDoc):
    """
        It is a Swagger doc for 'UserAnimeAPIView'
    """
    tags = [SwaggerTags.USER]

    responses = {
        status.HTTP_200_OK: openapi.Response(
            'Ok.',
            examples={
                'application/json':  {}
            },
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            'Bad request.',
            ResponseErrorSerializer,
            examples={
                'application/json': {
                    "errors": [
                        {
                            "message": 'Сталася помилка, спробуйте будь-ласка пізніше або'
                                       ' зверніться до адміністратора',
                        },
                    ]
                }
            },
        ),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(
            'Unauthorized.',
            examples={
                'application/json': {
                    "errors": [
                        {
                            "message": "Реквізити перевірки достовірності не надані.",
                        },
                    ]
                }
            },
        ),
    }


class UserViewedEpisodeAPIViewDoc(BaseSwaggerAPIViewDoc):
    """
        It is a Swagger doc for 'UserViewedEpisodeAPIView'
    """
    tags = [SwaggerTags.USER]

    responses = {
        status.HTTP_200_OK: openapi.Response(
            'Ok.',
            examples={
                'application/json':  {}
            },
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            'Bad request.',
            ResponseErrorSerializer,
            examples={
                'application/json': {
                    "errors": [
                        {
                            "message": 'Сталася помилка, спробуйте будь-ласка пізніше або'
                                       ' зверніться до адміністратора',
                        },
                    ]
                }
            },
        ),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(
            'Unauthorized.',
            examples={
                'application/json': {
                    "errors": [
                        {
                            "message": "Реквізити перевірки достовірності не надані.",
                        },
                    ]
                }
            },
        ),
    }
