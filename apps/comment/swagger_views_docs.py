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


