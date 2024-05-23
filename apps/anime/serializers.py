from rest_framework import serializers

from django.contrib.auth.models import Group

from apps.anime.models import (
    Director, Anime, Studio, Episode, PreviewImage, Genre, Voiceover, Poster
)


class DirectorSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    get_param = serializers.SerializerMethodField()
    filter_field = serializers.SerializerMethodField()

    class Meta:
        model = Director
        fields = ['value', 'filter_field', 'get_param']

    def get_value(self, obj: Director):
        return obj.full_name

    def get_filter_field(self, obj: Voiceover):
        return 'director'

    def get_get_param(self, obj: Voiceover):
        return obj.id


class GenreSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    get_param = serializers.SerializerMethodField()
    filter_field = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = ['value', 'filter_field', 'get_param']

    def get_value(self, obj: Genre):
        return obj.name

    def get_filter_field(self, obj: Voiceover):
        return 'genres'

    def get_get_param(self, obj: Voiceover):
        return obj.id


class StudioSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    get_param = serializers.SerializerMethodField()
    filter_field = serializers.SerializerMethodField()

    class Meta:
        model = Studio
        fields = ['value', 'filter_field', 'get_param']

    def get_value(self, obj: Studio):
        return obj.name

    def get_filter_field(self, obj: Voiceover):
        return 'studio'

    def get_get_param(self, obj: Voiceover):
        return obj.id


class ChildAnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anime
        fields = ['title', 'id', 'slug', 'card_image']


class VoiceoverSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    get_param = serializers.SerializerMethodField()
    filter_field = serializers.SerializerMethodField()

    class Meta:
        model = Voiceover
        fields = ['value', 'filter_field', 'get_param']

    def get_value(self, obj: Voiceover):
        return obj.team.name

    def get_filter_field(self, obj: Voiceover):
        return 'voiceover'

    def get_get_param(self, obj: Voiceover):
        return obj.team_id


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
        fields = ['anime', 'full_name']


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
    genres = GenreSerializer(many=True)
    year = serializers.SerializerMethodField()
    director = DirectorSerializer()
    studio = StudioSerializer()
    episodes_release_schedule = ChildEpisodesReleaseScheduleSerializer(
        many=True, source='get_episodes_release_schedule')
    count_episodes = serializers.IntegerField(source='get_count_episodes')
    voiceovers = serializers.ListSerializer(child=VoiceoverSerializer(), source='get_distinct_voiceover')
    status = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    season = serializers.SerializerMethodField()
    rating = serializers.CharField(source='get_rating_display')

    class Meta:
        model = Anime
        exclude = ['id', 'updated', 'created', 'slug']

    def get_year(self, obj: Anime):
        return obj.start_date.year

    def get_status(self, obj: Anime):
        return {
            'value': obj.get_status_display(),
            'filter_field': 'status',
            'get_param': obj.status,
        }

    def get_type(self, obj: Anime):
        return {
            'value': obj.get_type_display(),
            'filter_field': 'type',
            'get_param': obj.type,
        }

    def get_season(self, obj: Anime):
        return {
            'value': obj.get_season_display(),
            'filter_field': 'season',
            'get_param': obj.season,
        }


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
