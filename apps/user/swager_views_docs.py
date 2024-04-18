from drf_yasg import openapi
from rest_framework import status

from apps.core.swagger_views_docs import BaseSwaggerAPIViewDoc, SwaggerTags


class UserAPIViewDoc(BaseSwaggerAPIViewDoc):
    """
    It is a Swagger doc for 'UserAPIView'
    """
    tags = [SwaggerTags.USER]

    responses = {
        status.HTTP_200_OK: openapi.Response(
            'Ok.',
            examples={'application/json': {}},
        ),
    }
