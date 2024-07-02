from django.urls import path
from apps.user.views import (
    UserAPI, UserAnimeListAPIView, UserAddAnimeAPIView, UserViewedEpisodeAPIView
)


app_name = 'user'

urlpatterns = [
    path('', UserAPI.as_view()),
    path('anime/list/', UserAnimeListAPIView.as_view(), name='user-anime-list'),
    path('anime/add/', UserAddAnimeAPIView.as_view(), name='user-anime-add'),
    path('episode/viewed/', UserViewedEpisodeAPIView.as_view(), name='user-episode-viewed'),
]
