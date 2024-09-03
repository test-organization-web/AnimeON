from django_filters import rest_framework as filters

from apps.anime.models import Genre, Anime
from apps.anime.choices import AnimeTypes
from apps.user.choices import UserAnimeChoices


class UserAnimeListFilterSet(filters.FilterSet):
    genres = filters.ModelChoiceFilter(
        field_name='genres', to_field_name='id',
        queryset=Genre.objects.all()
    )
    type = filters.ChoiceFilter(
        field_name='type', choices=AnimeTypes.choices
    )
    name = filters.CharFilter(
        field_name='title', lookup_expr='contains',
    )
    action = filters.ChoiceFilter(
        field_name='useranime__action', choices=UserAnimeChoices.choices
    )

    class Meta:
        model = Anime
        fields = [
            'action', 'genres', 'type', 'name'
        ]
