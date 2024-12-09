from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.templatetags.static import static

from rest_framework import serializers

from apps.anime.models import Anime, Episode
from apps.user.models import UserAnime, UserSettings
from apps.user.choices import UserAnimeChoices
from apps.anime.serializers import ResponseAnimeListSerializer

UserModel = get_user_model()


class ResponseUserAnimeListSerializer(ResponseAnimeListSerializer):
    anime = ResponseAnimeListSerializer()

    class Meta:
        model = UserAnime
        fields = ['action', 'anime']


class ResponsePaginatedUserAnimeListSerializer(serializers.Serializer):
    active_page = serializers.IntegerField(allow_null=True)
    num_pages = serializers.IntegerField(allow_null=True)
    count = serializers.IntegerField(allow_null=True)
    next = serializers.URLField()
    previous = serializers.URLField()
    results = ResponseUserAnimeListSerializer(many=True)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    count_viewed_anime = serializers.IntegerField(source='get_count_viewed_anime')
    count_commented_anime = serializers.IntegerField(source='get_count_commented_anime')
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        fields = ('username', 'count_viewed_anime', 'count_commented_anime', 'avatar')

    def get_avatar(self, obj: UserModel):
        try:
            if avatar := obj.settings.avatar:
                return avatar.url
            return static('images/default_avatar.svg')
        except ObjectDoesNotExist:
            return static('images/default_avatar.svg')


class RequestUserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        exclude = ('user',)


class ResponseUserSettingsSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = UserSettings
        exclude = ('user', 'id')

    def get_avatar(self, obj: UserSettings):
        try:
            if avatar := obj.avatar:
                return avatar.url
            return static('images/default_avatar.svg')
        except ObjectDoesNotExist:
            return static('images/default_avatar.svg')


class RequestUserAnimeSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=UserAnimeChoices.choices)
    anime = serializers.PrimaryKeyRelatedField(
        queryset=Anime.objects.all(), error_messages={'does_not_exist': 'Аніме не знайдено.'}
    )


class RequestUserAnimeDeleteSerializer(serializers.Serializer):
    anime = serializers.PrimaryKeyRelatedField(
        queryset=Anime.objects.all(), error_messages={'does_not_exist': 'Аніме не знайдено.'}
    )


class RequestViewedEpisodeSerializer(serializers.Serializer):
    episode = serializers.PrimaryKeyRelatedField(
        queryset=Episode.objects.all(), error_messages={'does_not_exist': 'Епізод не знайдено.'}
    )
