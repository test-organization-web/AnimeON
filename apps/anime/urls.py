from django.urls import path
from apps.anime.views import (
    AnimeAPIView, AnimeListAPIView, AnimeSearchAPIView,
    PostersAnimeAPIView, FiltersAnimeAPIView, AnimeRandomAPIView,
    EpisodeAPIView, CommentAnimeAPIView, AnimeArchAPIView, AnimeReactAPIView
)


app_name = 'anime'


urlpatterns = [
    path('<int:pk>/<str:slug>/', AnimeAPIView.as_view(), name='get_anime'),
    path('<int:pk>/<str:slug>/comments/', CommentAnimeAPIView.as_view(), name='get_anime_comments'),
    path('<int:anime_pk>/<str:anime_slug>/episode/<int:order>/', EpisodeAPIView.as_view(),
         name='get_anime_episode'),
    path('list/', AnimeListAPIView.as_view(), name='get_anime_list'),
    path('random/', AnimeRandomAPIView.as_view(), name='get_random_anime'),
    path('search/', AnimeSearchAPIView.as_view(), name='search_anime'),
    path('posters/', PostersAnimeAPIView.as_view(), name='get_anime_posters'),
    path('filters/', FiltersAnimeAPIView.as_view(), name='get_anime_filters'),
    path('<int:pk>/<str:slug>/arch/', AnimeArchAPIView.as_view(), name='get_anime_arch'),
    path('<int:pk>/<str:slug>/reaction/', AnimeReactAPIView.as_view(), name='reaction_anime'),
]
