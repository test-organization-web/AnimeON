from drf_yasg import openapi
from rest_framework import status

from apps.core.swagger_views_docs import BaseSwaggerAPIViewDoc, SwaggerTags
from apps.anime.swagger_views_docs import CommentAnimeAPIViewDoc
from apps.core.serializers import ResponseErrorSerializer
from apps.anime.serializers import ResponseCommentAnimeSerializer
from apps.comment.serializers import ResponseCommentReactSerializer


class CommentCreateAPIViewDoc(BaseSwaggerAPIViewDoc):
    """
    It is a Swagger doc for 'CommentCreateAPIView'
    """
    tags = [SwaggerTags.COMMENT]

    responses = {
        status.HTTP_200_OK: openapi.Response(
            'Ok.',
            ResponseCommentAnimeSerializer,
            examples={'application/json': {
                "id": 13,
                "content_main": "string",
                "created": "2024-06-12T22:40:58.401294+03:00",
                "urlhash": "hunqbkxl",
                "has_reply": False,
                "get_count_like": 0,
                "get_count_dislike": 0,
                "username": "admin"
            }},
        ),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(
            'Unauthorized.',
            examples={
                'application/json': {
                    "detail": "Реквізити перевірки достовірності не надані."
                }
            },
        ),
        status.HTTP_403_FORBIDDEN: openapi.Response(
            'Forbidden.',
            ResponseErrorSerializer,
            examples={'application/json': {
                "errors": [
                    {
                        "message": "Спробуйте повторити запит через {N} секунд",
                    },
                ]
            }},
        ),
    }


class CommentReactAPIViewDoc(BaseSwaggerAPIViewDoc):
    tags = [SwaggerTags.COMMENT]

    responses = {
        status.HTTP_200_OK: openapi.Response(
            'Ok.',
            ResponseCommentReactSerializer,
            examples={'application/json': [
                {
                    'action': 'DELETE'
                },
                {
                    'action': 'CHANGE'
                },
                {
                    'action': 'NEW'
                },
            ]},
        ),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(
            'Unauthorized.',
            examples={
                'application/json': {
                    "detail": "Реквізити перевірки достовірності не надані."
                }
            },
        ),
    }


class ReplyCommentAPIViewDoc(CommentAnimeAPIViewDoc):
    """
        It is a Swagger doc for 'ReplyCommentAPIView'
    """
    tags = [SwaggerTags.COMMENT]
