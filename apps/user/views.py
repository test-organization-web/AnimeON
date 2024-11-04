import logging

from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from apps.core.utils import swagger_auto_schema_wrapper, validate_request_data, get_response_body_errors
from apps.user.swager_views_docs import (
    UserAPIViewDoc, UserAnimeListAPIViewDoc, UserAnimeAPIViewDoc, UserViewedEpisodeAPIViewDoc, UserSettingsAPIViewDoc,
    CreateUserSettingsAPIViewDoc,
)
from apps.user.serializers import (
    RequestUserAnimeSerializer, RequestViewedEpisodeSerializer, RequestUserAnimeDeleteSerializer,
    ResponseUserSettingsSerializer, UserSerializer, ResponseUserAnimeListSerializer, RequestUserSettingsSerializer
)
from apps.user.models import UserAnime, UserEpisodeViewed, UserSettings
from apps.user.filtersets import UserAnimeListFilterSet
from apps.user.paginators import UserAnimeListPaginator

logger = logging.getLogger(__name__)


class UserAPI(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    @swagger_auto_schema_wrapper(
        doc=UserAPIViewDoc,
        request_serializer_cls=None,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return self.request.user


class UserSettingsAPI(APIView):
    permission_classes = (IsAuthenticated,)
    response_serializer = ResponseUserSettingsSerializer
    request_serializer = RequestUserSettingsSerializer
    parser_classes = [MultiPartParser, FileUploadParser]

    @swagger_auto_schema_wrapper(
        doc=UserSettingsAPIViewDoc,
        request_serializer_cls=None,

    )
    def get(self, request, *args, **kwargs):
        settings = UserSettings.objects.filter(user=self.request.user).first()
        serializer = self.response_serializer(settings)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema_wrapper(
        doc=CreateUserSettingsAPIViewDoc,
        request_serializer_cls=request_serializer,
    )
    @validate_request_data(serializer_cls=request_serializer)
    def post(self, request, serializer: RequestUserSettingsSerializer):
        serializer_data = serializer.data
        with transaction.atomic():
            try:
                serializer_data.update({
                    'avatar': self.request.FILES['avatar'],
                })
                UserSettings.objects.update_or_create(
                    user=self.request.user,
                    defaults=serializer_data
                )
            except Exception as error:
                logger.exception(error)
                response_data = get_response_body_errors(errors='Сталася помилка, спробуйте будь-ласка'
                                                                ' пізніше або зверніться до адміністратора')
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status.HTTP_200_OK)


class UserAnimeAPIView(ListAPIView, APIView):
    permission_classes = (IsAuthenticated,)
    request_serializer = RequestUserAnimeSerializer
    request_delete_serializer = RequestUserAnimeDeleteSerializer

    queryset = UserAnime.objects.prefetch_related('anime__episode_set').all()

    serializer_class = ResponseUserAnimeListSerializer

    pagination_class = UserAnimeListPaginator

    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserAnimeListFilterSet

    @swagger_auto_schema_wrapper(
        doc=UserAnimeListAPIViewDoc,
        request_serializer_cls=None,
        operation_id='user_anime_list',
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        # Views have behaviour which varies dynamically based on request parameters
        # (using self.kwargs in their get_queryset, get_serializer, etc methods).
        # drf-yasg is unable to handle this because no requests are actually made to the inspected views.
        if getattr(self, "swagger_fake_view", False):
            # It means that the view instance was artificially created as part of a swagger schema request.
            return UserAnime.objects.none()
        return super().get_queryset().filter(user=self.request.user)

    @swagger_auto_schema_wrapper(doc=UserAnimeAPIViewDoc, request_serializer_cls=request_serializer,
                                 operation_id='user_add_anime',)
    @validate_request_data(serializer_cls=request_serializer)
    def post(self, request, serializer: RequestUserAnimeSerializer):
        anime = serializer.validated_data['anime']
        action = serializer.validated_data['action']
        with transaction.atomic():
            try:
                UserAnime.objects.update_or_create(
                    anime=anime,
                    user_id=request.user.id,
                    defaults=dict(
                        action=action
                    )
                )
            except Exception as error:
                logger.exception(error)
                response_data = get_response_body_errors(errors='Сталася помилка, спробуйте будь-ласка'
                                                                ' пізніше або зверніться до адміністратора')
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={}, status=status.HTTP_200_OK)

    @swagger_auto_schema_wrapper(doc=UserAnimeAPIViewDoc, request_serializer_cls=request_delete_serializer,
                                 operation_id='user_delete_anime', )
    @validate_request_data(serializer_cls=request_delete_serializer)
    def delete(self, request, serializer: RequestUserAnimeDeleteSerializer):
        anime = serializer.validated_data['anime']
        with transaction.atomic():
            try:
                UserAnime.objects.filter(
                    anime=anime,
                    user_id=request.user.id,
                ).delete()
            except Exception as error:
                logger.exception(error)
                response_data = get_response_body_errors(errors='Сталася помилка, спробуйте будь-ласка'
                                                                ' пізніше або зверніться до адміністратора')
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={}, status=status.HTTP_200_OK)


class UserViewedEpisodeAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    request_serializer = RequestViewedEpisodeSerializer

    @swagger_auto_schema_wrapper(doc=UserViewedEpisodeAPIViewDoc, request_serializer_cls=request_serializer,
                                 operation_id='user_add_viewed_episode',)
    @validate_request_data(serializer_cls=request_serializer)
    def post(self, request, serializer: RequestViewedEpisodeSerializer):
        episode = serializer.validated_data['episode']
        with transaction.atomic():
            try:
                UserEpisodeViewed.objects.get_or_create(
                    episode=episode,
                    user_id=request.user.id,
                )
            except Exception as error:
                logger.exception(error)
                response_data = get_response_body_errors(errors='Сталася помилка, спробуйте будь-ласка'
                                                                ' пізніше або зверніться до адміністратора')
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={}, status=status.HTTP_200_OK)
