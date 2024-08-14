from drf_yasg import openapi
from rest_framework import status

from apps.core.swagger_views_docs import BaseSwaggerAPIViewDoc, SwaggerTags


class RightholderAppealAPIViewDoc(BaseSwaggerAPIViewDoc):
    """
    It is a Swagger doc for 'RightholderAppealAPIView'
    """
    tags = [SwaggerTags.SUPPORT]

    responses = {
        status.HTTP_201_CREATED: openapi.Response(
            'Created.',
            examples={'application/json': {}},
        ),
    }


class HelpAppealAPIViewDoc(BaseSwaggerAPIViewDoc):
    """
    It is a Swagger doc for 'HelpAppealAPIView'
    """
    tags = [SwaggerTags.SUPPORT]

    responses = {
        status.HTTP_201_CREATED: openapi.Response(
            'Created.',
            examples={'application/json': {}},
        ),
    }