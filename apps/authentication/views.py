from django.contrib.auth import get_user_model
from django.contrib.auth import login

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginVie, LogoutView as KnoxLogoutView
from knox.models import AuthToken

from apps.core.utils import swagger_auto_schema_wrapper, validate_request_data
from apps.authentication.swagger_views_docs import (
    UserRegisterViewAPIViewDoc,
    UserLoginViewAPIViewDoc,
    UserLogoutViewAPIViewDoc,
)
from apps.authentication.serializers import UserRegisterSerializer
from apps.user.serializers import UserSerializer


class UserLogoutViewAPIView(KnoxLogoutView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema_wrapper(
        doc=UserLogoutViewAPIViewDoc,
    )
    def post(self, request, format=None):
        return super().post(request, format)


class UserLoginViewAPIView(KnoxLoginVie):
    permission_classes = (permissions.AllowAny,)
    serializer_class = AuthTokenSerializer

    @swagger_auto_schema_wrapper(
        doc=UserLoginViewAPIViewDoc,
        request_serializer_cls=serializer_class,
    )
    @validate_request_data(serializer_cls=serializer_class)
    def post(self, request, serializer: AuthTokenSerializer, format=None):
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
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
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })
