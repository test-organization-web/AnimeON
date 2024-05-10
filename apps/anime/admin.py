from django.contrib import admin
from django_admin_inline_paginator.admin import TabularInlinePaginated
from adminfilters.combo import RelatedFieldComboFilter, AllValuesComboFilter

from apps.anime.models import (
    Anime, Episode, Director, Studio, PreviewImage, Voiceover, VoiceoverHistory, Poster
)
from apps.core.admin import OnlyAddPermissionMixin, ReadOnlyPermissionsMixin, OnlyChangePermissionMixin

# Register your models here.


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
    list_display = ['name', 'country']
    inlines = [AnimeTabularInlinePaginated]

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
    list_display = ['title']
    inlines = [EpisodeTabularInlinePaginated, PreviewImageTabularInlinePaginated]
    list_filter = [
        ('genres', RelatedFieldComboFilter),
        ('studio', RelatedFieldComboFilter),
        ('director', RelatedFieldComboFilter),
        ('status', AllValuesComboFilter),
        ('type', AllValuesComboFilter),
        ('season', AllValuesComboFilter),
    ]

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
    list_display = ['anime', 'image']
