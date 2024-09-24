from drf_yasg import openapi
from rest_framework import status

from apps.core.swagger_views_docs import BaseSwaggerAPIViewDoc, SwaggerTags
from apps.authentication.serializers import (
    ResponseUserRegisterSerializer, ResponseUserLoginSerializer, ResponseUserLogoutSerializer
)
from apps.core.serializers import ResponseErrorSerializer


class UserRegisterViewAPIViewDoc(BaseSwaggerAPIViewDoc):
    """
    It is a Swagger doc for 'UserRegisterViewAPIView'
    """
    tags = [SwaggerTags.AUTH]

    responses = {
        status.HTTP_201_CREATED: openapi.Response(
            'Created.',
            ResponseUserRegisterSerializer,
            examples={'application/json': {
                "access": "<str: token>",
                "refresh": "<str: token>",
                "user": {
                    "username": "<str: username>"
                }
            }},
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            'Bad request.',
            ResponseErrorSerializer,
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
            ResponseUserLoginSerializer,
            examples={'application/json': {
                "access": "<str: token>",
                "refresh": "<str: token>",
                "user": {
                    "username": "<str: username>"
                }
            }},
        ),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(
            'Unauthorized.',
            ResponseErrorSerializer,
            examples={'application/json': {
                "errors": [
                    {
                        "message": "No active account found with the given credentials",
                    },
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
            ResponseUserLogoutSerializer,
            examples={'application/json': {
                "refresh": "<str: token>"
            }},
        ),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(
            'Unauthorized.',
            ResponseErrorSerializer,
            examples={'application/json': {
                "errors": [
                    {
                        "message": "No active account found with the given credentials",
                    },
                ]
            }}
        )
    }
