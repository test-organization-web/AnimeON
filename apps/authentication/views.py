import logging

from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import permissions, status
from rest_framework_simplejwt.tokens import RefreshToken, Token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenBlacklistView,
)
from rest_framework_simplejwt.serializers import TokenBlacklistSerializer
from rest_framework_simplejwt.exceptions import InvalidToken

from apps.core.utils import swagger_auto_schema_wrapper, validate_request_data, get_response_body_errors
from apps.authentication.swagger_views_docs import (
    UserRegisterViewAPIViewDoc,
    UserLoginViewAPIViewDoc,
    UserLogoutViewAPIViewDoc,
)
from apps.authentication.serializers import RequestUserRegisterSerializer, CustomTokenObtainPairSerializer
from apps.user.serializers import UserSerializer
from apps.core.debug import sensitive_drf_post_parameters


logger = logging.getLogger()


class UserLogoutViewAPIView(TokenBlacklistView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TokenBlacklistSerializer

    @swagger_auto_schema_wrapper(
        doc=UserLogoutViewAPIViewDoc,
        request_serializer_cls=serializer_class,
        operation_id='user_logout',
    )
    def post(self, request, format=None):
        try:
            logger.info('User try logout', extra={
                'message_id': 'authentication_logout_try'
            })
            return super().post(request, format)
        except InvalidToken:
            errors = get_response_body_errors(errors=InvalidToken.default_detail)
            return Response(data=errors, status=InvalidToken.status_code)


class UserLoginViewAPIView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer

    @swagger_auto_schema_wrapper(
        doc=UserLoginViewAPIViewDoc,
        request_serializer_cls=serializer_class,
        operation_id='user_login',
    )
    @validate_request_data(serializer_cls=serializer_class)
    def post(self, request, serializer: CustomTokenObtainPairSerializer, format=None):
        try:
            logger.info('User try login', extra={
                'message_id': 'authentication_login_try'
            })
            return super().post(request, format)
        except InvalidToken:
            errors = get_response_body_errors(errors=InvalidToken.default_detail)
            return Response(data=errors, status=InvalidToken.status_code)


class UserRegisterViewAPIView(GenericAPIView):
    model = get_user_model()
    permission_classes = (permissions.AllowAny,)  # Or anon users can't register
    serializer_class = RequestUserRegisterSerializer

    @method_decorator(sensitive_drf_post_parameters('password', 'password_repeat'))
    @swagger_auto_schema_wrapper(
        doc=UserRegisterViewAPIViewDoc,
        request_serializer_cls=serializer_class,
        operation_id='user_register',
    )
    @validate_request_data(serializer_cls=serializer_class)
    def post(self, request, serializer: RequestUserRegisterSerializer, *args, **kwargs):
        user = serializer.save()
        token: Token = RefreshToken.for_user(user)

        logger.info('User success register', extra={
            'message_id': 'authentication_register_success'
        })
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'refresh': str(token),
            'access': str(token.access_token),
        }, status=status.HTTP_201_CREATED)
