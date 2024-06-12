from drf_yasg import openapi
from rest_framework import status

from apps.core.swagger_views_docs import BaseSwaggerAPIViewDoc, SwaggerTags
from apps.anime.serializers import (
    ResponseDirectorSerializer, ResponseStudioSerializer, ResponseAnimeSerializer,
    ResponsePaginatedAnimeListSerializer, ResponsePostersSerializer, ResponseFiltersAnimeSerializer,
    ResponseAnimeRandomSerializer, ResponseAnimeEpisodeSerializer, ResponsePaginatedCommentAnimeListSerializer
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
                "full_name": "<str: full_name>",
                "url": "<str: url>",
                "anime": [
                    {
                        "title": "<str: title>",
                        "slug": "<str: slug>",
                        "id": 1,
                        "card_image": "<str: url>",
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
                        "title": "<str: title>",
                        "slug": "<str: slug>",
                        "id": 1,
                        "card_image": "<str: url>",
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
                "status": {
                    "value": "<str: value>",
                    "filter_url": "<str: url>",
                },
                "type": {
                    "value": "<str: value>",
                    "filter_url": "<str: url>",
                },
                "rating": "<str: rating>",
                "description": "<str: description>",
                "short_description": "<str: short_description>",
                "season": {
                    "value": "<str: value>",
                    "filter_url": "<str: url>",
                },
                "studio": {
                    "value": "<str: value>",
                    "filter_url": "<str: url>",
                },
                "related": None,
                "director": {
                    "value": "<str: value>",
                    "filter_url": "<str: url>",
                },
                "images": [
                    {
                        "file": "<str: url>",
                    }
                ],
                "genres": [
                    {
                        "value": "<str: value>",
                        "filter_url": "<str: url>",
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
                        "value": "<str: value>",
                        "filter_url": "<str: url>",
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
                        "value": "<str: value>",
                        "filter_url": "<str: url>",
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


class CommentAnimeAPIViewDoc(BaseSwaggerAPIViewDoc):
    """
        It is a Swagger doc for 'CommentAnimeAPIView'
    """
    tags = [SwaggerTags.ANIME]

    responses = {
        status.HTTP_200_OK: openapi.Response(
            'Ok.',
            ResponsePaginatedCommentAnimeListSerializer,
            examples={'application/json': {
                "active_page": 1,
                "num_pages": 1,
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": 13,
                        "content_main": "string",
                        "created": "2024-06-12T22:40:58.401294+03:00",
                        "urlhash": "hunqbkxl",
                        "has_reply": False,
                        "get_count_like": 0,
                        "get_count_dislike": 0,
                        "username": "admin"
                    }
                ]
            }},
        ),
    }
