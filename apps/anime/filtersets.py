from django_filters import rest_framework as filters
from django_countries import Countries

from django.contrib.auth.models import Group

from apps.anime.models import Anime, Genre, Studio, Director
from apps.anime.choices import AnimeTypes, SeasonTypes, AnimeStatuses


class AnimeListFilterSet(filters.FilterSet):
    genres = filters.ModelChoiceFilter(
        field_name='genres__name', to_field_name='name',
        queryset=Genre.objects.all()
    )
    studio = filters.ModelChoiceFilter(
        field_name='studio__name', to_field_name='name',
        queryset=Studio.objects.all()
    )
    country = filters.ChoiceFilter(
        field_name='studio__country', choices=Countries()
    )
    status = filters.ChoiceFilter(
        field_name='status', choices=AnimeStatuses.choices
    )
    director = filters.ModelChoiceFilter(
        field_name='director__pseudonym', to_field_name='pseudonym',
        queryset=Director.objects.all()
    )
    type = filters.ChoiceFilter(
        field_name='type', choices=AnimeTypes.choices
    )
    voiceover = filters.ModelChoiceFilter(
        field_name='episode__voiceover__team__name', to_field_name='name',
        queryset=Group.objects.all()
    )
    season = filters.ChoiceFilter(
        field_name='season', choices=SeasonTypes.choices
    )
    year_gte = filters.DateFilter(
        field_name='start_date__year', lookup_expr='gte'
    )
    year_lte = filters.DateFilter(
        field_name='start_date__year', lookup_expr='lte'
    )

    class Meta:
        model = Anime
        fields = [
            'genres', 'studio', 'country', 'status', 'director', 'type', 'voiceover', 'season',
            'year_gte', 'year_lte'
        ]
