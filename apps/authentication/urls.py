from django.urls import path
from apps.authentication import views


app_name = 'authentication'


urlpatterns = [
    path('login/', views.UserLoginViewAPIView.as_view(), name='login'),
    path("registration/", views.UserRegisterViewAPIView.as_view(), name="register"),
    path('logout/', views.UserLogoutViewAPIView.as_view(), name='logout')
]