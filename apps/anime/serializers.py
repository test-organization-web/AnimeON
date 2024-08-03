from rest_framework import serializers

from django.contrib.auth.models import Group
from django.urls import reverse
from django.http import QueryDict

from apps.anime.models import (
    Director, Anime, Studio, Episode, PreviewImage, Genre, Voiceover, Poster
)
from apps.comment.models import Comment


class DirectorSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    filter_url = serializers.SerializerMethodField()

    class Meta:
        model = Director
        fields = ['value', 'filter_url']

    def get_value(self, obj: Director):
        return obj.full_name

    def get_filter_url(self, obj: Director):
        get_params = QueryDict(f'director={obj.id}')
        return f"{reverse('anime:get_anime_list')}?{get_params.urlencode()}"


class GenreSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    filter_url = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = ['value', 'filter_url']

    def get_value(self, obj: Genre):
        return obj.name

    def get_filter_url(self, obj: Genre):
        get_params = QueryDict(f'genres={obj.id}')
        return f"{reverse('anime:get_anime_list')}?{get_params.urlencode()}"


class StudioSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    filter_url = serializers.SerializerMethodField()

    class Meta:
        model = Studio
        fields = ['value', 'filter_url']

    def get_value(self, obj: Studio):
        return obj.name

    def get_filter_url(self, obj: Studio):
        get_params = QueryDict(f'studio={obj.id}')
        return f"{reverse('anime:get_anime_list')}?{get_params.urlencode()}"


class ChildAnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anime
        fields = ['title', 'id', 'slug', 'card_image']


class VoiceoverSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    filter_url = serializers.SerializerMethodField()

    class Meta:
        model = Voiceover
        fields = ['value', 'filter_url']

    def get_value(self, obj: Voiceover):
        return obj.team.name

    def get_filter_url(self, obj: Voiceover):
        get_params = QueryDict(f'voiceover={obj.team_id}')
        return f"{reverse('anime:get_anime_list')}?{get_params.urlencode()}"


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
        fields = ['title', 'order', 'release_date', 'status']


class ResponseAnimeListSerializer(serializers.ModelSerializer):
    year = serializers.SerializerMethodField()
    count_episodes = serializers.SerializerMethodField()
    genres = ChildGenreSerializer(many=True)

    class Meta:
        model = Anime
        fields = [
            'id', 'slug', 'title', 'count_episodes', 'type', 'year', 'rating', 'genres', 'card_image'
        ]

    def get_count_episodes(self, obj: Anime):
        return obj.count_episodes

    def get_year(self, obj: Anime):
        return obj.start_date.year


class ResponseAnimeSerializer(serializers.ModelSerializer):
    episodes = serializers.ListSerializer(child=ChildEpisodeSerializer(), source='episode_set')
    images = serializers.ListSerializer(child=ChildPreviewImageSerializer(),
                                        source='previewimage_set')
    genres = GenreSerializer(many=True)
    director = DirectorSerializer()
    studio = StudioSerializer(many=True, read_only=True)
    episodes_release_schedule = ChildEpisodesReleaseScheduleSerializer(
        many=True, source='get_episodes_release_schedule')
    voiceovers = serializers.ListSerializer(child=VoiceoverSerializer(),
                                            source='get_distinct_voiceover')
    status = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    season = serializers.SerializerMethodField()
    rating = serializers.CharField(source='get_rating_display')
    country = serializers.CharField(source='get_country_display')
    related = ResponseAnimeListSerializer(many=True, read_only=True)

    class Meta:
        model = Anime
        exclude = ['id', 'updated', 'created', 'slug']

    def get_year(self, obj: Anime):
        return obj.start_date.year

    def get_status(self, obj: Anime):
        get_params = QueryDict(f'status={obj.status}')
        return {
            'value': obj.get_status_display(),
            'filter_url': f"{reverse('anime:get_anime_list')}?{get_params.urlencode()}",
        }

    def get_type(self, obj: Anime):
        get_params = QueryDict(f'type={obj.type}')
        return {
            'value': obj.get_type_display(),
            'filter_url': f"{reverse('anime:get_anime_list')}?{get_params.urlencode()}",
        }

    def get_season(self, obj: Anime):
        get_params = QueryDict(f'season={obj.season}')
        return {
            'value': obj.get_season_display(),
            'filter_url': f"{reverse('anime:get_anime_list')}?{get_params.urlencode()}",
        }


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


class ResponseAnimeEpisodeSerializer(serializers.ModelSerializer):
    voiceover = VoiceoverSerializer(source='voiceovers', many=True, read_only=True)
    subtitles = VoiceoverSerializer(many=True, read_only=True)

    class Meta:
        model = Episode
        fields = ['title', 'voiceover', 'subtitles', 'preview_image', 'youtube_url',
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
