from rest_framework import serializers

from django.contrib.auth.models import Group

from apps.anime.models import (
    Director, Anime, Studio, Episode, PreviewImage, Genre, Voiceover, Poster
)


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        exclude = []


class StudioSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source='get_country_display')

    class Meta:
        model = Studio
        exclude = []


class ChildAnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anime
        fields = ['title']


class VoiceoverSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField()

    class Meta:
        model = Voiceover
        fields = ['url', 'team']

    def get_team(self, obj: Voiceover):
        return obj.team.name


class ChildEpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ['title', 'order']


class ChildPreviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreviewImage
        fields = ['file']


class ChildGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']


class ResponseDirectorSerializer(serializers.ModelSerializer):
    anime = serializers.ListSerializer(child=ChildAnimeSerializer(), source='anime_set')

    class Meta:
        model = Director
        exclude = ['id']


class ResponseStudioSerializer(serializers.ModelSerializer):
    anime = serializers.ListSerializer(child=ChildAnimeSerializer(), source='anime_set')

    class Meta:
        model = Studio
        exclude = ['id']


class ChildEpisodesReleaseScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ['title', 'order', 'release_date']


class ResponseAnimeSerializer(serializers.ModelSerializer):
    episodes = serializers.ListSerializer(child=ChildEpisodeSerializer(), source='episode_set')
    images = serializers.ListSerializer(child=ChildPreviewImageSerializer(), source='previewimage_set')
    genres = ChildGenreSerializer(many=True)
    year = serializers.SerializerMethodField()
    director = DirectorSerializer()
    studio = StudioSerializer()
    episodes_release_schedule = ChildEpisodesReleaseScheduleSerializer(
        many=True, source='get_episodes_release_schedule')
    count_episodes = serializers.IntegerField(source='get_count_episodes')
    voiceovers = serializers.ListSerializer(child=VoiceoverSerializer(), source='get_distinct_voiceover')
    status = serializers.CharField(source='get_status_display')
    type = serializers.CharField(source='get_type_display')
    season = serializers.CharField(source='get_season_display')
    rating = serializers.CharField(source='get_rating_display')

    class Meta:
        model = Anime
        exclude = ['id', 'updated', 'created', 'slug']

    def get_year(self, obj: Anime):
        return obj.start_date.year


class ResponseAnimeListSerializer(serializers.ModelSerializer):
    count_episodes = serializers.IntegerField(source='get_count_episodes')
    year = serializers.SerializerMethodField()
    genres = ChildGenreSerializer(many=True)

    class Meta:
        model = Anime
        fields = [
            'id', 'slug', 'title', 'count_episodes', 'type', 'year', 'rating', 'genres', 'card_image'
        ]

    def get_year(self, obj: Anime):
        return obj.start_date.year


class ChildPaginatedAnimeSerializer(ResponseAnimeListSerializer):
    pass


class ResponsePaginatedAnimeListSerializer(serializers.Serializer):
    active_page = serializers.IntegerField(allow_null=True)
    num_pages = serializers.IntegerField(allow_null=True)
    count = serializers.IntegerField(allow_null=True)
    next = serializers.URLField()
    previous = serializers.URLField()
    results = ChildPaginatedAnimeSerializer(many=True)


class ChildAnimePosterSerializer(serializers.ModelSerializer):
    count_episodes = serializers.IntegerField(source='get_count_episodes')

    class Meta:
        model = Anime
        fields = [
            'id', 'slug', 'title', 'count_episodes'
        ]


class ResponsePostersSerializer(serializers.ModelSerializer):
    anime = ChildAnimePosterSerializer(read_only=True)

    class Meta:
        model = Poster
        fields = [
            'anime', 'image', 'description'
        ]


class ResponseListDirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'full_name']


class ResponseListStudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = ['id', 'name']


class ResponseListVoiceoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class ResponseListGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class ResponseFiltersAnimeSerializer(serializers.Serializer):
    directors = serializers.JSONField()
    genres = serializers.JSONField()
    studios = serializers.JSONField()
    countries = serializers.JSONField()
    voiceover = serializers.JSONField()
    status = serializers.JSONField()
    type = serializers.JSONField()
    season = serializers.JSONField()


class ResponseAnimeRandomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anime
        fields = ['id', 'slug']


class ResponseAnimeEpisodeSerializer(serializers.ModelSerializer):
    voiceover = VoiceoverSerializer(source='voiceovers', many=True, read_only=True)
    subtitles = VoiceoverSerializer(many=True, read_only=True)

    class Meta:
        model = Episode
        fields = ['title', 'voiceover', 'subtitles']
