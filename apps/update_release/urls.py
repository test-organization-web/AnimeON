from django.urls import path
from apps.update_release.callback import myanimelist


app_name = 'update_release'


urlpatterns = [
    path('callback/myanimelist/', myanimelist.callback, name='callback_myanimelist'),
]