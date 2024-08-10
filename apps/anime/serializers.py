from rest_framework import serializers

from django.http import QueryDict

from apps.anime.models import (
    Director, Anime, Studio, Episode, PreviewImage, Genre, Voiceover, Poster, Arch
)
from apps.comment.models import Comment
from apps.user.models import Group


class DirectorSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    get_params = serializers.SerializerMethodField()

    class Meta:
        model = Director
        fields = ['value', 'get_params']

    def get_value(self, obj: Director):
        return obj.full_name

    def get_get_params(self, obj: Director):
        get_params = QueryDict(f'director={obj.id}')
        return get_params.urlencode()


class GenreSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    get_params = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = ['value', 'get_params']

    def get_value(self, obj: Genre):
        return obj.name

    def get_get_params(self, obj: Genre):
        get_params = QueryDict(f'genres={obj.id}')
        return get_params.urlencode()


class StudioSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    get_params = serializers.SerializerMethodField()

    class Meta:
        model = Studio
        fields = ['value', 'get_params']

    def get_value(self, obj: Studio):
        return obj.name

    def get_get_params(self, obj: Studio):
        get_params = QueryDict(f'studio={obj.id}')
        return get_params.urlencode()


class ResponseAnimeListSerializer(serializers.ModelSerializer):
    count_episodes = serializers.SerializerMethodField()

    class Meta:
        model = Anime
        fields = [
            'id', 'slug', 'title', 'count_episodes', 'type', 'year', 'card_image'
        ]

    def get_count_episodes(self, obj: Anime):
        return obj.episode_set.all().count()


class ChildTeamSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    get_params = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['value', 'get_params']

    def get_value(self, obj: Group):
        return obj.name

    def get_get_params(self, obj: Group):
        get_params = QueryDict(f'voiceover={obj.id}')
        return get_params.urlencode()


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
    anime = serializers.ListSerializer(child=ResponseAnimeListSerializer(), source='anime_set')

    class Meta:
        model = Director
        fields = ['anime', 'full_name']


class ResponseStudioSerializer(serializers.ModelSerializer):
    anime = serializers.ListSerializer(child=ResponseAnimeListSerializer(), source='anime_set')

    class Meta:
        model = Studio
        exclude = ['id']


class ChildEpisodesReleaseScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ['title', 'order', 'release_date', 'status']


class ResponseAnimeSerializer(serializers.ModelSerializer):
    episodes = serializers.ListSerializer(child=ChildEpisodeSerializer(), source='episode_set')
    images = serializers.ListSerializer(child=ChildPreviewImageSerializer(),
                                        source='previewimage_set')
    genres = GenreSerializer(many=True, read_only=True)
    director = DirectorSerializer()
    studio = StudioSerializer(many=True, read_only=True)
    voiceovers = serializers.ListSerializer(child=ChildTeamSerializer(), source='get_distinct_team')
    status = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    season = serializers.SerializerMethodField()
    rating = serializers.CharField(source='get_rating_display')
    country = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    count_episodes = serializers.SerializerMethodField()
    similar = serializers.ListSerializer(child=ResponseAnimeListSerializer(), source='get_similar')

    class Meta:
        model = Anime
        exclude = ['id', 'updated', 'created', 'slug', 'is_top']

    def get_count_episodes(self, obj: Anime):
        return {
            'value': obj.count_episodes,
            'get_params': '',
        }

    def get_year(self, obj: Anime):
        get_params = QueryDict(f'year={obj.year}')
        return {
            'value': obj.year,
            'get_params': get_params.urlencode(),
        }

    def get_country(self, obj: Anime):
        get_params = QueryDict(f'country={obj.country}')
        return {
            'value': obj.get_country_display(),
            'get_params': get_params.urlencode(),
        }

    def get_status(self, obj: Anime):
        get_params = QueryDict(f'status={obj.status}')
        return {
            'value': obj.get_status_display(),
            'get_params': get_params.urlencode(),
        }

    def get_type(self, obj: Anime):
        get_params = QueryDict(f'type={obj.type}')
        return {
            'value': obj.get_type_display(),
            'get_params': get_params.urlencode(),
        }

    def get_season(self, obj: Anime):
        get_params = QueryDict(f'season={obj.season}')
        return {
            'value': obj.get_season_display(),
            'get_params': get_params.urlencode(),
        }


class ResponsePaginatedAnimeListSerializer(serializers.Serializer):
    active_page = serializers.IntegerField(allow_null=True)
    num_pages = serializers.IntegerField(allow_null=True)
    count = serializers.IntegerField(allow_null=True)
    next = serializers.URLField()
    previous = serializers.URLField()
    results = ResponseAnimeListSerializer(many=True)


class ChildAnimePosterSerializer(serializers.ModelSerializer):
    count_episodes = serializers.SerializerMethodField()

    class Meta:
        model = Anime
        fields = [
            'id', 'slug', 'title', 'count_episodes'
        ]

    def get_count_episodes(self, obj: Anime):
        return obj.episode_set.all().count()


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


class EpisodeVoiceoverSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()

    class Meta:
        model = Voiceover
        fields = ['value', 'url']

    def get_value(self, obj: Voiceover):
        return obj.team.name


class ResponseAnimeEpisodeSerializer(serializers.ModelSerializer):
    voiceover = EpisodeVoiceoverSerializer(source='voiceovers', many=True, read_only=True)
    subtitles = EpisodeVoiceoverSerializer(many=True, read_only=True)

    class Meta:
        model = Episode
        fields = ['title', 'voiceover', 'subtitles', 'preview_image',
                  'start_opening', 'end_opening', 'start_ending', 'end_ending']


class ResponseCommentAnimeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Comment
        fields = ('id', 'content_main', 'created', 'urlhash', 'has_reply', 'get_count_like',
                  'get_count_dislike', 'username')


class ResponsePaginatedCommentAnimeListSerializer(serializers.Serializer):
    active_page = serializers.IntegerField(allow_null=True)
    num_pages = serializers.IntegerField(allow_null=True)
    count = serializers.IntegerField(allow_null=True)
    next = serializers.URLField()
    previous = serializers.URLField()
    results = ResponseCommentAnimeSerializer(many=True)


class ResponseAnimeArchSerializer(serializers.ModelSerializer):
    episodes = serializers.ListSerializer(child=ChildEpisodeSerializer(), source='episode_set')

    class Meta:
        model = Arch
        fields = ['order', 'title', 'episodes']
