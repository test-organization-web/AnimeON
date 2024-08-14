from django.urls import path

from apps.support.views import RightholderAppealAPIView, HelpAppealAPIView


app_name = 'support'

urlpatterns = [
    path('rightholder/', RightholderAppealAPIView.as_view(), name='create-rightholder-appeal'),
    path('help/', HelpAppealAPIView.as_view(), name='create-help-appeal'),
]
