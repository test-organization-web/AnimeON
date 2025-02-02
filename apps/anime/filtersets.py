from django_filters import rest_framework as filters
from django_countries import Countries

from django.contrib.auth.models import Group

from apps.anime.models import Anime, Genre, Studio, Director
from apps.anime.choices import AnimeTypes, SeasonTypes, AnimeStatuses


class AnimeListFilterSet(filters.FilterSet):
    order_by = filters.OrderingFilter(
        choices=(
            ('created', 'Created'),
            ('-created', 'Created(-)'),
            ('is_popular', 'Popular'),
            ('-is_popular', 'Popular(-)'),
        ),
        fields={
            'created': 'created',
            '-created': '-created',
            'count_like': 'is_popular',
            '-count_like': '-is_popular',
        },
    )
    genres = filters.ModelChoiceFilter(
        field_name='genres', to_field_name='id',
        queryset=Genre.objects.all()
    )
    studio = filters.ModelMultipleChoiceFilter(
        field_name='studio', to_field_name='id',
        queryset=Studio.objects.all()
    )
    country = filters.ChoiceFilter(
        field_name='country', choices=Countries()
    )
    status = filters.ChoiceFilter(
        field_name='status', choices=AnimeStatuses.choices
    )
    director = filters.ModelChoiceFilter(
        field_name='director_id', to_field_name='id',
        queryset=Director.objects.all()
    )
    type = filters.ChoiceFilter(
        field_name='type', choices=AnimeTypes.choices
    )
    voiceover = filters.ModelChoiceFilter(
        field_name='episode__voiceover__team_id', to_field_name='id',
        queryset=Group.objects.all()
    )
    season = filters.ChoiceFilter(
        field_name='season', choices=SeasonTypes.choices
    )
    year_gte = filters.NumberFilter(
        field_name='start_date__year', lookup_expr='gte'
    )
    year_lte = filters.NumberFilter(
        field_name='start_date__year', lookup_expr='lte'
    )
    episode_gte = filters.NumberFilter(
        field_name='count_episodes', lookup_expr='gte'
    )
    episode_lte = filters.NumberFilter(
        field_name='count_episodes', lookup_expr='lte'
    )

    class Meta:
        model = Anime
        fields = [
            'genres', 'studio', 'country', 'status', 'director', 'type', 'voiceover', 'season',
            'year_gte', 'year_lte', 'episode_lte', 'episode_gte'
        ]
