from django_filters import rest_framework as filters

from apps.anime.models import Genre
from apps.anime.choices import AnimeTypes
from apps.user.choices import UserAnimeChoices
from apps.user.models import UserAnime


class UserAnimeListFilterSet(filters.FilterSet):
    genres = filters.ModelChoiceFilter(
        field_name='anime__genres', to_field_name='id',
        queryset=Genre.objects.all()
    )
    type = filters.ChoiceFilter(
        field_name='anime__type', choices=AnimeTypes.choices
    )
    name = filters.CharFilter(
        field_name='anime__title', lookup_expr='contains',
    )
    action = filters.ChoiceFilter(
        field_name='action', choices=UserAnimeChoices.choices
    )

    class Meta:
        model = UserAnime
        fields = [
            'action', 'genres', 'type', 'name'
        ]
