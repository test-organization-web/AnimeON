from drf_yasg import openapi
from rest_framework import status

from apps.core.swagger_views_docs import BaseSwaggerAPIViewDoc, SwaggerTags
from apps.anime.swagger_views_docs import CommentAnimeAPIViewDoc
from apps.comment.serializers import CommentReactSerializer, CreateCommentSerializer


class CommentCreateAPIViewDoc(BaseSwaggerAPIViewDoc):
    """
    It is a Swagger doc for 'CommentCreateAPIView'
    """
    tags = [SwaggerTags.COMMENT]

    responses = {
        status.HTTP_200_OK: openapi.Response(
            'Ok.',
            CreateCommentSerializer,
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
    }


class CommentReactAPIViewDoc(BaseSwaggerAPIViewDoc):
    tags = [SwaggerTags.COMMENT]

    responses = {
        status.HTTP_200_OK: openapi.Response(
            'Ok.',
            CommentReactSerializer,
            examples={'application/json': {

            }},
        ),
    }


