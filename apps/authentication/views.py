from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenBlacklistView,
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenBlacklistSerializer

from apps.core.utils import swagger_auto_schema_wrapper, validate_request_data
from apps.authentication.swagger_views_docs import (
    UserRegisterViewAPIViewDoc,
    UserLoginViewAPIViewDoc,
    UserLogoutViewAPIViewDoc,
)
from apps.authentication.serializers import UserRegisterSerializer
from apps.user.serializers import UserSerializer


class UserLogoutViewAPIView(TokenBlacklistView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = TokenBlacklistSerializer

    @swagger_auto_schema_wrapper(
        doc=UserLogoutViewAPIViewDoc,
        request_serializer_cls=serializer_class,
    )
    def post(self, request, format=None):
        return super().post(request, format)


class UserLoginViewAPIView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = TokenObtainPairSerializer

    @swagger_auto_schema_wrapper(
        doc=UserLoginViewAPIViewDoc,
        request_serializer_cls=serializer_class,
    )
    @validate_request_data(serializer_cls=serializer_class)
    def post(self, request, serializer: TokenObtainPairSerializer, format=None):
        return super().post(request, format)


class UserRegisterViewAPIView(GenericAPIView):
    model = get_user_model()
    permission_classes = (permissions.AllowAny,)  # Or anon users can't register
    serializer_class = UserRegisterSerializer

    @swagger_auto_schema_wrapper(
        doc=UserRegisterViewAPIViewDoc,
        request_serializer_cls=UserRegisterSerializer,
    )
    @validate_request_data(serializer_cls=UserRegisterSerializer)
    def post(self, request, serializer: UserRegisterSerializer, *args, **kwargs):
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'refresh': str(token),
            'access': str(token.access_token),
        }, status=status.HTTP_201_CREATED)
