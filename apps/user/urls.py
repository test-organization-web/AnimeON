from django.urls import path
from apps.user.views import (
    UserAPI, UserAnimeAPIView, UserViewedEpisodeAPIView, UserSettingsAPI
)


app_name = 'user'

urlpatterns = [
    path('', UserAPI.as_view(), name='user'),
    path('settings/', UserSettingsAPI.as_view(), name='user-settings'),
    path('anime/', UserAnimeAPIView.as_view(), name='user-anime'),
    path('episode/viewed/', UserViewedEpisodeAPIView.as_view(), name='user-episode-viewed'),
]
