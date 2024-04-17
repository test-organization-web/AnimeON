from drf_yasg import openapi
from rest_framework import status

from apps.core.swagger_views_docs import BaseSwaggerAPIViewDoc, SwaggerTags


class UserRegisterViewAPIViewDoc(BaseSwaggerAPIViewDoc):
    """
    It is a Swagger doc for 'UserRegisterViewAPIView'
    """
    tags = [SwaggerTags.AUTH]

    responses = {
        status.HTTP_200_OK: openapi.Response(
            'Ok.',
            examples={'application/json': {
                "user": {
                    "username": "username"
                },
                "token": "<str: token>"
            }},
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            'Bad request.',
            examples={'application/json': {
                "errors": [
                    {
                        "message": "This field is required.",
                        "location": "username"
                    },
                    {
                        "message": "This field is required.",
                        "location": "email"
                    },
                    {
                        "message": "A user with that username already exists.",
                        "location": "username"
                    },
                    {
                        "message": "A user with this email already exists.",
                        "location": "email"
                    },
                    {
                        "message": "This field is required.",
                        "location": "email"
                    },
                    {
                        "message": "Password Does not match",
                        "location": "password"
                    },
                    {
                        "message": "Email already exist",
                        "location": "email"
                    }
                ]
            }},
        ),
    }


class UserLoginViewAPIViewDoc(BaseSwaggerAPIViewDoc):
    """
        It is a Swagger doc for 'UserLoginViewAPIView'
        """
    tags = [SwaggerTags.AUTH]

    responses = {
        status.HTTP_200_OK: openapi.Response(
            'Ok.',
            examples={'application/json': {}},
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            'Bad request.',
            examples={'application/json': {
                "errors": [
                    {
                        "message": "Unable to log in with provided credentials.",
                        "location": "non_field_errors"
                    }
                ]
            }},
        )
    }


class UserLogoutViewAPIViewDoc(BaseSwaggerAPIViewDoc):
    """
        It is a Swagger doc for 'UserLogoutViewAPIView'
        """
    tags = [SwaggerTags.AUTH]

    responses = {
        status.HTTP_200_OK: openapi.Response(
            'Ok.',
            examples={'application/json': {}},
        ),
    }
