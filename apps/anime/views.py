import logging
from typing import Union, List, Tuple
from collections import OrderedDict

from rest_framework.generics import RetrieveAPIView, ListAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework import permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from django_countries.data import COUNTRIES

from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType

from apps.anime.serializers import (
    ResponseDirectorSerializer, ResponseStudioSerializer, ResponseAnimeSerializer, ResponseAnimeListSerializer,
    ResponsePostersSerializer, ResponseFiltersAnimeSerializer, ResponseAnimeRandomSerializer,
    ResponseAnimeEpisodeSerializer, ResponseCommentAnimeSerializer, ResponseAnimeArchSerializer
)
from apps.core.utils import swagger_auto_schema_wrapper
from apps.anime.swagger_views_docs import (
    DirectorAPIViewDoc, StudioAPIViewDoc, AnimeAPIViewDoc, AnimeListAPIViewDoc, AnimeSearchAPIViewDoc,
    AnimeTOP100APIViewDoc, PostersAnimeAPIViewDoc, FiltersAnimeAPIViewDoc,
    AnimeRandomAPIViewDoc, ResponseAnimeEpisodeAPIViewDoc, CommentAnimeAPIViewDoc,
    AnimeArchAPIViewDoc
)
from apps.anime.models import Director, Studio, Anime, Poster, Episode, Genre, Arch
from apps.anime.paginators import AnimeListPaginator
from apps.anime.filtersets import AnimeListFilterSet
from apps.anime.choices import AnimeStatuses, AnimeTypes, SeasonTypes

from apps.comment.paginators import CommentAnimeListPaginator
from apps.comment.models import Comment


logger = logging.getLogger()


class DirectorAPIView(RetrieveAPIView):
    queryset = Director.objects.all()
    serializer_class = ResponseDirectorSerializer

    @swagger_auto_schema_wrapper(
        doc=DirectorAPIViewDoc,
        operation_id='get_director',
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class StudioAPIView(RetrieveAPIView):
    queryset = Studio.objects.all()
    serializer_class = ResponseStudioSerializer

    @swagger_auto_schema_wrapper(
        doc=StudioAPIViewDoc,
        operation_id='get_studio',
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AnimeAPIView(RetrieveAPIView):
    queryset = Anime.objects.prefetch_related(
        'genres', 'director', 'studio', 'episode_set', 'previewimage_set'
    ).all()
    serializer_class = ResponseAnimeSerializer

    @swagger_auto_schema_wrapper(
        doc=AnimeAPIViewDoc,
        operation_id='get_anime',
    )
    def get(self, request, slug, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AnimeSearchAPIView(ListAPIView):
    queryset = Anime.objects.prefetch_related('episode_set').all()
    serializer_class = ResponseAnimeListSerializer
    pagination_class = AnimeListPaginator

    filter_backends = (SearchFilter,)
    search_fields = ['title']

    @swagger_auto_schema_wrapper(
        doc=AnimeSearchAPIViewDoc,
        operation_id='search_anime',
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AnimeListAPIView(ListAPIView):
    permission_classes = [permissions.AllowAny]

    queryset = Anime.objects.prefetch_related('episode_set').all()
    serializer_class = ResponseAnimeListSerializer
    pagination_class = AnimeListPaginator

    filter_backends = (DjangoFilterBackend,)
    filterset_class = AnimeListFilterSet

    @swagger_auto_schema_wrapper(
        doc=AnimeListAPIViewDoc,
        operation_id='get_anime_list',
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AnimeRandomAPIView(RetrieveAPIView):
    queryset = Anime.objects.all().order_by('?')
    serializer_class = ResponseAnimeRandomSerializer

    def get_object(self):
        return self.get_queryset().first()

    @swagger_auto_schema_wrapper(
        doc=AnimeRandomAPIViewDoc,
        operation_id='get_random_anime',
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AnimeTOP100APIView(ListAPIView):
    queryset = Anime.objects.prefetch_related('episode_set').filter(is_top=True)
    serializer_class = ResponseAnimeListSerializer
    pagination_class = AnimeListPaginator

    @swagger_auto_schema_wrapper(
        doc=AnimeTOP100APIViewDoc,
        operation_id='get_top_100_anime',
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PostersAnimeAPIView(ListAPIView):
    queryset = Poster.objects.prefetch_related('anime', 'anime__episode_set').all()
    serializer_class = ResponsePostersSerializer

    @swagger_auto_schema_wrapper(
        doc=PostersAnimeAPIViewDoc,
        operation_id='get_anime_posters',
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class FiltersAnimeAPIView(GenericAPIView):
    default_all = {'': 'Всі'}
    response_serializer = ResponseFiltersAnimeSerializer

    def add_option_all(self, options: Union[List[Tuple[int, str]], dict]) -> dict:
        if isinstance(options, dict):
            options = list(options.items())
        d = OrderedDict(options)
        d.update(self.default_all)
        d.move_to_end('', last=False)
        return d

    @swagger_auto_schema_wrapper(
        doc=FiltersAnimeAPIViewDoc,
        operation_id='get_anime_filters',
    )
    def get(self, request, *args, **kwargs):
        directors = list((director.id, director.full_name) for director in Director.objects.all())
        genres = list((genre.id, genre.name) for genre in Genre.objects.all())
        studios = list((studio.id, studio.name) for studio in Studio.objects.all())
        voiceover = list((group.id, group.name) for group in Group.objects.all())
        response = self.response_serializer({
            'directors': self.add_option_all(directors),
            'genres': self.add_option_all(genres),
            'studios': self.add_option_all(studios),
            'countries': self.add_option_all(COUNTRIES),
            'voiceover': self.add_option_all(voiceover),
            'status': self.add_option_all(list(AnimeStatuses.choices)),
            'type': self.add_option_all(list(AnimeTypes.choices)),
            'season': self.add_option_all(list(SeasonTypes.choices)),
        }).data
        return Response(data=response, status=status.HTTP_200_OK)


class EpisodeAPIView(RetrieveAPIView):
    lookup_field = 'anime_id'
    lookup_url_kwarg = 'anime_pk'
    queryset = Episode.objects.prefetch_related('voiceover_set', 'voiceover_set__team').all()
    serializer_class = ResponseAnimeEpisodeSerializer

    def get_queryset(self):
        # Views have behaviour which varies dynamically based on request parameters
        # (using self.kwargs in their get_queryset, get_serializer, etc methods).
        # drf-yasg is unable to handle this because no requests are actually made to the inspected views.
        if getattr(self, "swagger_fake_view", False):
            # It means that the view instance was artificially created as part of a swagger schema request.
            return Episode.objects.none()
        episode_order = self.kwargs['order']
        return super().get_queryset().filter(order=episode_order)

    @swagger_auto_schema_wrapper(
        doc=ResponseAnimeEpisodeAPIViewDoc,
        operation_id='get_anime_episode',
    )
    def get(self, request, *args, **kwargs):
        return super().get(request)


class CommentAnimeAPIView(ListAPIView):
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'

    permission_classes = (permissions.AllowAny,)  # Or anon users can't register

    serializer_class = ResponseCommentAnimeSerializer
    pagination_class = CommentAnimeListPaginator

    @swagger_auto_schema_wrapper(
        doc=CommentAnimeAPIViewDoc,
        operation_id='get_anime_comments',
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        # Views have behaviour which varies dynamically based on request parameters
        # (using self.kwargs in their get_queryset, get_serializer, etc methods).
        # drf-yasg is unable to handle this because no requests are actually made to the inspected views.
        if getattr(self, "swagger_fake_view", False):
            # It means that the view instance was artificially created as part of a swagger schema request.
            return Comment.objects.none()

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        content_type = ContentType.objects.get(app_label='anime', model='anime')
        queryset = Comment.objects.filter(
            content_type=content_type, object_id=self.kwargs[lookup_url_kwarg]
        )
        return queryset.filter_parents()


class AnimeArchAPIView(ListAPIView):
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'

    serializer_class = ResponseAnimeArchSerializer

    @swagger_auto_schema_wrapper(
        doc=AnimeArchAPIViewDoc,
        operation_id='get_anime_arche',
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        # Views have behaviour which varies dynamically based on request parameters
        # (using self.kwargs in their get_queryset, get_serializer, etc methods).
        # drf-yasg is unable to handle this because no requests are actually made to the inspected views.
        if getattr(self, "swagger_fake_view", False):
            # It means that the view instance was artificially created as part of a swagger schema request.
            return Arch.objects.none()

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        return Arch.objects.prefetch_related('anime__episode_set').filter(
            anime_id=self.kwargs[lookup_url_kwarg]
        ).order_by('order')
