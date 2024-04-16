from django.urls import path
from .views import CustomAuthToken

app_name = 'user'

urlpatterns = [
    path('token/', CustomAuthToken.as_view(), name='crate-auth-token'),
]
