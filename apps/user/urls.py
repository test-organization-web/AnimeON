from django.urls import path
from apps.user.views import UserAPI, SettingsAPI

app_name = 'user'

urlpatterns = [
    path('', UserAPI.as_view()),
    path('settings/', SettingsAPI.as_view()),
]
