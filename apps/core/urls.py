from django.urls import path
from apps.core.views import CountryAutocomplete


app_name = 'core'

urlpatterns = [
    path('country-autocomplete/', CountryAutocomplete.as_view(), name='country-list-autocomplete'),
]
