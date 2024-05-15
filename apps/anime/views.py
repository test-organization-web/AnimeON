import logging
from typing import Union, List, Tuple
from collections import OrderedDict

from rest_framework.generics import RetrieveAPIView, ListAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django_countries.data import COUNTRIES

from django.contrib.auth.models import Group

from apps.anime.serializers import (
    ResponseDirectorSerializer, ResponseStudioSerializer, ResponseAnimeSerializer, ResponseAnimeListSerializer,
    ResponsePostersSerializer, ResponseFiltersAnimeSerializer, ResponseAnimeRandomSerializer,
    ResponseAnimeEpisodeSerializer
)
from apps.core.utils import swagger_auto_schema_wrapper
from apps.anime.swagger_views_docs import (
    DirectorAPIViewDoc, StudioAPIViewDoc, AnimeAPIViewDoc, AnimeListAPIViewDoc, AnimeSearchAPIViewDoc,
    AnimeListRandomAPIViewDoc, AnimeTOP100APIViewDoc, PostersAnimeAPIViewDoc, FiltersAnimeAPIViewDoc,
    AnimeRandomAPIViewDoc, ResponseAnimeEpisodeAPIViewDoc,
)
from apps.anime.models import Director, Studio, Anime, Poster, Episode, Genre
from apps.anime.paginators import AnimeListPaginator
from apps.anime.filtersets import AnimeListFilterSet
from apps.anime.choices import AnimeStatuses, AnimeTypes, SeasonTypes


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
    queryset = Anime.objects.all()
    serializer_class = ResponseAnimeSerializer

    @swagger_auto_schema_wrapper(
        doc=AnimeAPIViewDoc,
        operation_id='get_anime',
    )
    def get(self, request, slug, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AnimeSearchAPIView(ListAPIView):
    queryset = Anime.objects.all()
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
    queryset = Anime.objects.all()
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


class AnimeListRandomAPIView(ListAPIView):
    queryset = Anime.objects.all().order_by('?')
    serializer_class = ResponseAnimeListSerializer
    pagination_class = AnimeListPaginator

    @swagger_auto_schema_wrapper(
        doc=AnimeListRandomAPIViewDoc,
        operation_id='get_anime_list_random',
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
    queryset = Anime.objects.filter(is_top=True)
    serializer_class = ResponseAnimeListSerializer
    pagination_class = AnimeListPaginator

    @swagger_auto_schema_wrapper(
        doc=AnimeTOP100APIViewDoc,
        operation_id='get_top_100_anime',
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PostersAnimeAPIView(ListAPIView):
    queryset = Poster.objects.all()
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
    queryset = Episode.objects.all()
    serializer_class = ResponseAnimeEpisodeSerializer

    def get_queryset(self):
        anime_pk = self.kwargs['anime_pk']
        return super().get_queryset().filter(anime_id=anime_pk)

    @swagger_auto_schema_wrapper(
        doc=ResponseAnimeEpisodeAPIViewDoc,
        operation_id='get_anime_episode',
    )
    def get(self, request, *args, **kwargs):
        return super().get(request)
