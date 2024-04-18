from drf_yasg import openapi
from rest_framework import status

from apps.core.swagger_views_docs import BaseSwaggerAPIViewDoc, SwaggerTags
from apps.anime.serializers import (
    ResponseDirectorSerializer, ResponseStudioSerializer, ResponseAnimeSerializer,
    ResponsePaginatedAnimeListSerializer, ResponsePostersSerializer, ResponseFiltersAnimeSerializer,
    ResponseAnimeRandomSerializer, ResponseAnimeEpisodeSerializer
)


class DirectorAPIViewDoc(BaseSwaggerAPIViewDoc):
    """
    It is a Swagger doc for 'DirectorAPIView'
    """
    tags = [SwaggerTags.ANIME]

    responses = {
        status.HTTP_200_OK: openapi.Response(
            'Ok.',
            ResponseDirectorSerializer,
            examples={'application/json': {
                "first_name": "<str: first_name>",
                "last_name": "<str: last_name>",
                "pseudonym": "<str: pseudonym>",
                "url": "<str: url>",
                "anime": [
                    {
                        "title": "<str: title>"
                    }
                ],
            }},
        ),
    }


class StudioAPIViewDoc(BaseSwaggerAPIViewDoc):
    """
    It is a Swagger doc for 'StudioAPIView'
    """
    tags = [SwaggerTags.ANIME]

    responses = {
        status.HTTP_200_OK: openapi.Response(
            'Ok.',
            ResponseStudioSerializer,
            examples={'application/json': {
                "anime": [
                    {
                        "title": "<str: title>"
                    }
                ],
                "created": "<str: created>",
                "name": "<str: name>",
                "description": "<str: description>",
                "country": "<str: country>"
            }},
        ),
    }


class AnimeAPIViewDoc(BaseSwaggerAPIViewDoc):
    """
    It is a Swagger doc for 'AnimeAPIView'
    """
    tags = [SwaggerTags.ANIME]

    responses = {
        status.HTTP_200_OK: openapi.Response(
            'Ok.',
            ResponseAnimeSerializer,
            examples={'application/json': {
                "episodes": [
                    {
                        "title": "<str: title>",
                        "order": 1
                    }
                ],
                "title": "<str: title>",
                "start_date": "<str: start_date>",
                "end_date": None,
                "rank": 1,
                "status": "<str: status>",
                "rating": "<str: rating>",
                "description": "<str: description>",
                "short_description": "<str: short_description>",
                "season": "<str: studio>",
                "studio": "<str: studio>",
                "related": None,
                "director": "<str: director>",
                "images": [
                    {
                        "file": "<str: url>",
                    }
                ],
                "genres": [
                    {
                        "name": "<str: genres>"
                    }
                ],
                "card_image": "<str: url>",
                "background_image": "<str: url>",
                "episodes_release_schedule": [
                    {
                        "title": "<str: title>",
                        "order": 0,
                        "release_date": "<str: release_date>"
                    }
                ],
                "voiceovers": [
                    {
                        "url": "<str: url>",
                        "team": "<str: team>",
                    }
                ]
            }},
        ),
    }


class AnimeListAPIViewDoc(BaseSwaggerAPIViewDoc):
    """
    It is a Swagger doc for 'AnimeListAPIView'
    """
    tags = [SwaggerTags.ANIME]

    responses = {
        status.HTTP_200_OK: openapi.Response(
            'Ok.',
            ResponsePaginatedAnimeListSerializer,
            examples={'application/json': {
                "active_page": 1,
                "num_pages": 1,
                "count": 1,
                "next": "<str: url>",
                "previous": "<str: url>",
                "results": [
                    {
                        "id": 1,
                        "slug": "<str: slug>",
                        "title": "<str: title>",
                        "start_date": "<str: start_date>",
                        "count_episodes": 1,
                        "type": "<str: type>",
                        "card_image": "<str: url>",
                    }
                ]
            }},
        ),
    }


class AnimeSearchAPIViewDoc(BaseSwaggerAPIViewDoc):
    """
    It is a Swagger doc for 'AnimeSearchAPIView'
    """
    tags = [SwaggerTags.ANIME]

    responses = {
        status.HTTP_200_OK: openapi.Response(
            'Ok.',
            ResponsePaginatedAnimeListSerializer,
            examples={'application/json': {
                "active_page": 1,
                "num_pages": 1,
                "count": 1,
                "next": "<str: url>",
                "previous": "<str: url>",
                "results": [
                    {
                        "id": 1,
                        "slug": "<str: slug>",
                        "title": "<str: title>",
                        "start_date": "<str: start_date>",
                        "count_episodes": 1,
                        "type": "<str: type>",
                        "card_image": "<str: url>",
                    }
                ]
            }},
        ),
    }


class AnimeListRandomAPIViewDoc(BaseSwaggerAPIViewDoc):
    """
    It is a Swagger doc for 'AnimeListRandomAPIView'
    """
    tags = [SwaggerTags.ANIME]

    responses = {
        status.HTTP_200_OK: openapi.Response(
            'Ok.',
            ResponsePaginatedAnimeListSerializer,
            examples={'application/json': {
                "active_page": 1,
                "num_pages": 1,
                "count": 1,
                "next": "<str: url>",
                "previous": "<str: url>",
                "results": [
                    {
                        "id": 1,
                        "slug": "<str: slug>",
                        "title": "<str: title>",
                        "start_date": "<str: start_date>",
                        "count_episodes": 1,
                        "type": "<str: type>",
                        "card_image": "<str: url>",
                    }
                ]
            }},
        ),
    }


class AnimeTOP100APIViewDoc(BaseSwaggerAPIViewDoc):
    """
    It is a Swagger doc for 'AnimeTOP100APIView'
    """
    tags = [SwaggerTags.ANIME]

    responses = {
        status.HTTP_200_OK: openapi.Response(
            'Ok.',
            ResponsePaginatedAnimeListSerializer,
            examples={'application/json': {
                "active_page": 1,
                "num_pages": 1,
                "count": 1,
                "next": "<str: url>",
                "previous": "<str: url>",
                "results": [
                    {
                        "id": 1,
                        "slug": "<str: slug>",
                        "title": "<str: title>",
                        "start_date": "<str: start_date>",
                        "count_episodes": 1,
                        "type": "<str: type>",
                        "card_image": "<str: url>",
                        "main_image": {
                            "file": "<str: url>",
                            "is_main": True,
                        }
                    }
                ]
            }},
        ),
    }


class PostersAnimeAPIViewDoc(BaseSwaggerAPIViewDoc):
    """
    It is a Swagger doc for 'PostersAnimeAPIViewDoc'
    """
    tags = [SwaggerTags.ANIME]

    responses = {
        status.HTTP_200_OK: openapi.Response(
            'Ok.',
            ResponsePostersSerializer,
            examples={'application/json': [
                {
                    "anime": {
                        "id": 23,
                        "slug": "<str: slug>",
                        "title": "<str: title>",
                        "count_episodes": 1
                    },
                    "image": "<str: url>",
                    "description": "<str: description>"
                }
            ]},
        ),
    }


class FiltersAnimeAPIViewDoc(BaseSwaggerAPIViewDoc):
    """
        It is a Swagger doc for 'FiltersAnimeAPIViewDoc'
    """
    tags = [SwaggerTags.ANIME]

    responses = {
        status.HTTP_200_OK: openapi.Response(
            'Ok.',
            ResponseFiltersAnimeSerializer,
            examples={'application/json': [
                {
                    'directors': [
                        {
                            1: "<str: name>",
                        }
                    ],
                    'studios': [
                        {
                            1: "<str: name>",
                        }
                    ],
                    'genres': [
                        {
                            1: "<str: name>",
                        }
                    ],
                    "countries": {
                        "AI": "Anguilla",
                    },
                    "voiceover": [{
                        "id": 1,
                        "name": "Anguilla",
                    }],
                    "status": {
                        "CAME_OUT": "Вийшов",
                        "COMES_OUT": "Виходить",
                        "ANNOUNCED": "Анонсовано"
                    },
                    "type": {
                        "ANIME": "Аніме",
                        "FILM": "Фільм"
                    },
                    "season": {
                        'WINTER': 'Зима',
                        'SPRING': 'Весна',
                        'SUMMER': 'Літо',
                        'FALL': 'Осінь',
                    }
                }
            ]},
        ),
    }


class AnimeRandomAPIViewDoc(BaseSwaggerAPIViewDoc):
    """
        It is a Swagger doc for 'AnimeRandomAPIView'
    """
    tags = [SwaggerTags.ANIME]

    responses = {
        status.HTTP_200_OK: openapi.Response(
            'Ok.',
            ResponseAnimeRandomSerializer,
            examples={'application/json': {
                'id': 1,
                'slug': '<str: slug>'
            }},
        ),
    }


class ResponseAnimeEpisodeAPIViewDoc(BaseSwaggerAPIViewDoc):
    """
        It is a Swagger doc for 'ResponseAnimeEpisodeAPIView'
    """
    tags = [SwaggerTags.ANIME]

    responses = {
        status.HTTP_200_OK: openapi.Response(
            'Ok.',
            ResponseAnimeEpisodeSerializer,
            examples={'application/json': {
                "title": "<str: title>",
                "voiceover": [
                    {
                        "url": "<str: url>",
                        "team": "<str: name>"
                    }
                ],
                "subtitles": [
                    {
                        "url": "<str: url>",
                        "team": "<str: name>"
                    }
                ]
            }},
        ),
    }
