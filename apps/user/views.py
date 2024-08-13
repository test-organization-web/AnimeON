import logging
from drf_yasg import openapi

from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from apps.user.serializers import UserSerializer
from apps.core.utils import swagger_auto_schema_wrapper, validate_request_data, get_response_body_errors
from apps.user.swager_views_docs import (
    UserAPIViewDoc, UserAnimeAPIViewDoc, UserAddAnimeAPIViewDoc, UserViewedEpisodeAPIViewDoc,
)
from apps.user.serializers import UserAnimeSerializer, RequestUserAnimeSerializer, RequestViewedEpisodeSerializer
from apps.user.choices import UserAnimeChoices
from apps.user.models import UserAnime, UserEpisodeViewed

logger = logging.getLogger(__name__)


class UserAPI(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    @swagger_auto_schema_wrapper(
        doc=UserAPIViewDoc,
        request_serializer_cls=None
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return self.request.user


class UserAnimeListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserAnimeSerializer

    @swagger_auto_schema_wrapper(
        doc=UserAnimeAPIViewDoc,
        manual_parameters=[
            openapi.Parameter('action', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False)
        ],
        request_serializer_cls=None
    )
    def get(self, request, *args, **kwargs):
        action = request.query_params.get('action', None)
        user = self.request.user

        if action and action in UserAnimeChoices.values:
            user_anime = UserAnime.objects.prefetch_related(
                'anime', 'anime__episode_set'
            ).filter(user_id=user.id, action=action)
        else:
            user_anime = UserAnime.objects.prefetch_related(
                'anime', 'anime__episode_set'
            ).filter(user_id=user.id)

        serializer = self.get_serializer(user_anime, many=True)
        return Response(serializer.data)


class UserAddAnimeAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    request_serializer = RequestUserAnimeSerializer

    @swagger_auto_schema_wrapper(doc=UserAddAnimeAPIViewDoc, request_serializer_cls=request_serializer,
                                 operation_id='user_add_anime',)
    @validate_request_data(serializer_cls=request_serializer)
    def post(self, request, serializer: RequestUserAnimeSerializer):
        anime = serializer.validated_data['anime']
        action = serializer.validated_data['action']
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


class UserViewedEpisodeAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    request_serializer = RequestViewedEpisodeSerializer

    @swagger_auto_schema_wrapper(doc=UserViewedEpisodeAPIViewDoc, request_serializer_cls=request_serializer,
                                 operation_id='user_add_viewed_episode',)
    @validate_request_data(serializer_cls=request_serializer)
    def post(self, request, serializer: RequestViewedEpisodeSerializer):
        episode = serializer.validated_data['episode']
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
