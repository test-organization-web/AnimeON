from django import forms
from django_countries.data import COUNTRIES
from dal import autocomplete

from apps.anime.models import Anime


class AnimeAdminForm(forms.ModelForm):
    country = autocomplete.Select2ListChoiceField(
        choice_list=[[code, name] for code, name in COUNTRIES.items()],
        widget=autocomplete.ListSelect2(url='core:country-list-autocomplete')
    )

    class Meta:
        model = Anime
        fields = '__all__'
