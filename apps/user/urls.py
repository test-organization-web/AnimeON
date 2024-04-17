from django.urls import path
from apps.user.views import UserAPI

app_name = 'user'

urlpatterns = [
    path('', UserAPI.as_view()),
]
