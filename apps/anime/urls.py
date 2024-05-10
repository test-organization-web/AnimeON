from django.urls import path
from apps.anime.views import (
    DirectorAPIView, StudioAPIView, AnimeAPIView, AnimeListAPIView, AnimeSearchAPIView,
    AnimeListRandomAPIView, PostersAnimeAPIView, FiltersAnimeAPIView, AnimeRandomAPIView,
    EpisodeAPIView
)


app_name = 'anime'


urlpatterns = [
    path('director/<int:pk>/', DirectorAPIView.as_view(), name='get_director'),
    path('studio/<int:pk>/', StudioAPIView.as_view(), name='get_studio'),
    path('<int:pk>/<str:slug>/', AnimeAPIView.as_view(), name='get_anime'),
    path('<int:anime_pk>/episode/<int:pk>/', EpisodeAPIView.as_view(), name='get_anime_episode'),
    path('list/', AnimeListAPIView.as_view(), name='get_anime_list'),
    path('list/random/', AnimeListRandomAPIView.as_view(), name='get_anime_list_random'),
    path('random/', AnimeRandomAPIView.as_view(), name='get_random_anime'),
    path('search/', AnimeSearchAPIView.as_view(), name='search_anime'),
    path('posters/', PostersAnimeAPIView.as_view(), name='get_anime_posters'),
    path('filters/', FiltersAnimeAPIView.as_view(), name='get_anime_filters'),
]
