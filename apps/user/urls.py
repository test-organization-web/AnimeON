from django.urls import path
from apps.user.views import UserAPI, UserAnimeCountAPI

app_name = 'user'

urlpatterns = [
    path('', UserAPI.as_view()),
    path('user/anime-count/', UserAnimeCountAPI.as_view(), name='user-anime-count'),

]
