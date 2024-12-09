from rest_framework import serializers

from django.http import QueryDict
from django.template.defaultfilters import date as _date
from django.core.exceptions import ObjectDoesNotExist
from django.templatetags.static import static

from apps.anime.models import (
    Director, Anime, Studio, Episode, PreviewImage, Genre, Voiceover, Poster, Arch, Reaction
)
from apps.anime.choices import ReactionChoices
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
        return QueryDict(f'director={obj.id}').urlencode()


class GenreSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    get_params = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = ['value', 'get_params']

    def get_value(self, obj: Genre):
        return obj.name

    def get_get_params(self, obj: Genre):
        return QueryDict(f'genres={obj.id}').urlencode()


class StudioSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    get_params = serializers.SerializerMethodField()

    class Meta:
        model = Studio
        fields = ['value', 'get_params']

    def get_value(self, obj: Studio):
        return obj.name

    def get_get_params(self, obj: Studio):
        return QueryDict(f'studio={obj.id}').urlencode()


class ResponseAnimeListSerializer(serializers.ModelSerializer):
    count_episodes = serializers.SerializerMethodField()

    class Meta:
        model = Anime
        fields = [
            'id', 'slug', 'title', 'count_episodes', 'type', 'year', 'card_image'
        ]

    def get_count_episodes(self, obj: Anime):
        return obj.episode_set.count()


class ChildTeamSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    get_params = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['value', 'get_params', 'avatar']

    def get_value(self, obj: Group):
        return obj.name

    def get_get_params(self, obj: Group):
        return QueryDict(f'voiceover={obj.id}').urlencode()

    def get_avatar(self, obj: Group):
        try:
            if avatar := obj.settings.avatar:
                return avatar.url
            return static('images/default_avatar.svg')
        except ObjectDoesNotExist:
            return static('images/default_avatar.svg')


class ChildEpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ['title', 'order', 'id']


class ChildPreviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreviewImage
        fields = ['file']


class ChildGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']


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
    count_episodes = serializers.SerializerMethodField()
    similar = serializers.ListSerializer(child=ResponseAnimeListSerializer(), source='get_similar')
    start_date = serializers.SerializerMethodField()
    reactions = serializers.SerializerMethodField()

    class Meta:
        model = Anime
        exclude = ['updated', 'created', 'is_top']

    def get_start_date(self, obj: Anime):
        start_date_str = _date(obj.start_date, 'd F Y')
        start_params = {
            'value': f'з {start_date_str}',
            'get_params': QueryDict(f'year_gte={obj.start_date.year}').urlencode(),
        }
        end_params = {}
        if obj.end_date:
            end_date_str = _date(obj.end_date, 'd F Y')
            end_params = {
                'value': f'no {end_date_str}',
                'get_params': QueryDict(f'year_lte={obj.end_date.year}').urlencode(),
            }
        return [start_params, end_params] if end_params else start_params

    def get_count_episodes(self, obj: Anime):
        count_episodes = obj.episode_set.count()
        return {
            'value': count_episodes,
            'get_params': QueryDict(f'episode_lte={count_episodes}').urlencode(),
        }

    def get_country(self, obj: Anime):
        return {
            'value': obj.get_country_display(),
            'get_params': QueryDict(f'country={obj.country}').urlencode(),
        }

    def get_status(self, obj: Anime):
        return {
            'value': obj.get_status_display(),
            'get_params': QueryDict(f'status={obj.status}').urlencode(),
        }

    def get_type(self, obj: Anime):
        return {
            'value': obj.get_type_display(),
            'get_params': QueryDict(f'type={obj.type}').urlencode(),
        }

    def get_season(self, obj: Anime):
        return {
            'value': obj.get_season_display(),
            'get_params': QueryDict(f'season={obj.season}').urlencode(),
        }

    def get_reactions(self, obj: Anime):
        return {
            reaction: obj.get_count_by_reaction(reaction=reaction) for reaction in ReactionChoices.values
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
        return obj.episode_set.count()


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
    voiceover = EpisodeVoiceoverSerializer(source='public_voiceovers', many=True, read_only=True)
    subtitles = EpisodeVoiceoverSerializer(source='public_subtitles', many=True, read_only=True)

    class Meta:
        model = Episode
        fields = ['title', 'voiceover', 'subtitles', 'preview_image', 'id',
                  'start_opening', 'end_opening', 'start_ending', 'end_ending']


class ResponseCommentAnimeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'content_main', 'created', 'urlhash', 'has_reply', 'get_count_like',
                  'get_count_dislike', 'username', 'avatar')

    def get_avatar(self, obj: Comment):
        try:
            if avatar := obj.user.settings.avatar:
                return avatar.url
            return static('images/default_avatar.svg')
        except ObjectDoesNotExist:
            return static('images/default_avatar.svg')


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


class AnimeReactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ('reaction',)


class ResponseAnimeReactSerializer(serializers.Serializer):
    action = serializers.ChoiceField(
        choices=(('DELETE', 'DELETE'), ('CHANGE', 'CHANGE'), ('NEW', 'NEW'))
    )
