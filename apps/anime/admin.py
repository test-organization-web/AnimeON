from django.utils import timezone
from django.contrib import admin
from django.utils.html import format_html

from django_admin_inline_paginator.admin import TabularInlinePaginated
from adminfilters.combo import RelatedFieldComboFilter, AllValuesComboFilter
from rangefilter.filters import NumericRangeFilter

from apps.anime.models import (
    Anime, Episode, Director, Studio, PreviewImage, Voiceover, VoiceoverHistory, Poster, Genre
)
from apps.core.admin import OnlyAddPermissionMixin, ReadOnlyPermissionsMixin, OnlyChangePermissionMixin
from apps.anime.choices import VoiceoverHistoryEvents

# Register your models here.


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']


class AnimeTabularInlinePaginated(ReadOnlyPermissionsMixin, TabularInlinePaginated):
    model = Anime
    show_change_link = True
    extra = 0
    fields = ['title']


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name', 'pseudonym')
    search_help_text = 'Search by First name, Last name, Pseudonym'
    list_display = ['first_name', 'last_name', 'pseudonym', 'url']
    inlines = [AnimeTabularInlinePaginated]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('anime_set')


@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    search_help_text = 'Search by Name'
    list_display = ['name']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('anime_set')


class EpisodeTabularInlinePaginated(ReadOnlyPermissionsMixin, TabularInlinePaginated):
    model = Episode
    show_change_link = True
    extra = 0
    fields = ['title', 'order', 'arch']


class PreviewImageTabularInlinePaginated(OnlyAddPermissionMixin, TabularInlinePaginated):
    model = PreviewImage
    show_change_link = True
    extra = 0


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    search_fields = ('title', )
    search_help_text = 'Search by Title'
    list_display = ['display_poster', 'title', 'display_count_episodes', 'display_type',
                    'display_season', 'year']
    inlines = [EpisodeTabularInlinePaginated, PreviewImageTabularInlinePaginated]
    list_filter = [
        ('genres', RelatedFieldComboFilter),
        ('studio', RelatedFieldComboFilter),
        ('director', RelatedFieldComboFilter),
        ('status', AllValuesComboFilter),
        ('type', AllValuesComboFilter),
        ('season', AllValuesComboFilter),
        ('year', NumericRangeFilter),
        ('release_day_of_week', AllValuesComboFilter),
        ('rating', AllValuesComboFilter),
    ]

    class Media:
        css = {
            'all': (
                "//code.jquery.com/ui/1.11.1/themes/smoothness/jquery-ui.css",
                'admin/css/utils/modal.css',
                'admin/css/buttons.css',
            )
        }
        js = (
            '//code.jquery.com/jquery-1.11.1.min.js',
            '//code.jquery.com/ui/1.11.1/jquery-ui.min.js',
            '//cdn.jsdelivr.net/npm/js-cookie@3.0.1/dist/js.cookie.min.js',
            "admin/js/utils/modal.js",
            "admin/js/utils/add_modal.js",
        )

    @admin.display(description='Poster', ordering='type')
    def display_poster(self, obj: Anime):
        if not obj.card_image:
            return self.get_empty_value_display()
        return format_html(
            '<img style="height: 100px; width: 50px;" src="{url}">',
            url=obj.card_image.url
        )

    @admin.display(description='Type', ordering='type')
    def display_type(self, obj: Anime):
        return obj.get_type_display()

    @admin.display(description='Season', ordering='season')
    def display_season(self, obj: Anime):
        return obj.get_season_display()

    @admin.display(description='Episodes')
    def display_count_episodes(self, obj: Anime):
        return obj.count_episodes

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            'genres', 'director', 'related', 'studio', 'episode_set',
        )


class VoiceoverTabularInlinePaginated(ReadOnlyPermissionsMixin, TabularInlinePaginated):
    model = Voiceover
    show_change_link = True


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    search_fields = ('anime__title',)
    search_help_text = 'Search by Anime'
    list_display = ['title', 'display_arch_title', 'anime']
    inlines = [VoiceoverTabularInlinePaginated]

    list_filter = [
        ('anime', RelatedFieldComboFilter),
        ('order', AllValuesComboFilter),
        ('status', AllValuesComboFilter),
    ]

    @admin.display()
    def display_arch_title(self, obj: Episode):
        return obj.arch.title if obj.arch else self.get_empty_value_display()

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('voiceover_set')


class VoiceoverHistoryInline(ReadOnlyPermissionsMixin, TabularInlinePaginated):
    model = VoiceoverHistory
    extra = 0


@admin.register(Voiceover)
class VoiceoverAdmin(admin.ModelAdmin):
    search_fields = ('episode__anime__title',)
    search_help_text = 'Search by Anime'
    list_display = ['episode', 'team', 'user', 'type', 'status', 'verified']
    inlines = [VoiceoverHistoryInline]

    list_filter = [
        'verified',
        ('episode', RelatedFieldComboFilter),
        ('team', RelatedFieldComboFilter),
        ('type', AllValuesComboFilter),
        ('status', AllValuesComboFilter),
    ]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change:
            obj.process_new_history_event(
                user=request.user,
                event=VoiceoverHistoryEvents.CHANGED,
            )
        else:
            obj.process_new_history_event(
                event=VoiceoverHistoryEvents.CREATED,
                user=request.user,
                created=timezone.now()
            )


class TOP100(Anime):
    class Meta:
        proxy = True
        verbose_name = 'Top 100'
        verbose_name_plural = 'Top 100'


@admin.register(TOP100)
class TOP100Admin(OnlyChangePermissionMixin, admin.ModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_top=True)


@admin.register(Poster)
class PosterAdmin(admin.ModelAdmin):
    list_display = ['anime', 'display_poster']

    @admin.display(description='Poster')
    def display_poster(self, obj: Poster):
        if not obj.image:
            return self.get_empty_value_display()
        return format_html(
            '<img style="height: 100px; width: 50px;" src="{url}">',
            url=obj.image.url
        )
