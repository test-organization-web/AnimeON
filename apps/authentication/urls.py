from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from apps.authentication import views

app_name = 'authentication'


urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('login/', views.UserLoginViewAPIView.as_view(), name='login'),
    path("registration/", views.UserRegisterViewAPIView.as_view(), name="register"),
    path('logout/', views.UserLogoutViewAPIView.as_view(), name='logout')
]