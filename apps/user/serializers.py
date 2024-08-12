from django.contrib.auth import get_user_model

from rest_framework import serializers

from apps.user.models import UserAnime
from apps.anime.models import Anime, Episode
from apps.user.choices import UserAnimeChoices

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    count_viewed_anime = serializers.CharField(source='get_count_viewed_anime')
    count_commented_anime = serializers.CharField(source='get_count_commented_anime')

    class Meta:
        model = UserModel
        fields = ('username', 'count_viewed_anime', 'count_commented_anime')


class AnimeSerializer(serializers.ModelSerializer):
    count_episodes = serializers.SerializerMethodField()

    class Meta:
        model = Anime
        fields = [
            'id', 'slug', 'title', 'count_episodes', 'card_image'
        ]

    def get_count_episodes(self, obj: Anime):
        return obj.episode_set.all().count()


class UserAnimeSerializer(serializers.ModelSerializer):
    anime = AnimeSerializer()

    class Meta:
        model = UserAnime
        fields = ('anime',)


class RequestUserAnimeSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=UserAnimeChoices.choices)
    anime = serializers.PrimaryKeyRelatedField(
        queryset=Anime.objects.all(), error_messages={'does_not_exist': 'Аніме не знайдено.'}
    )


class RequestViewedEpisodeSerializer(serializers.Serializer):
    episode = serializers.PrimaryKeyRelatedField(
        queryset=Episode.objects.all(), error_messages={'does_not_exist': 'Епізод не знайдено.'}
    )
