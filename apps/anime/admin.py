from django.utils import timezone
from django.contrib import admin
from django.utils.html import format_html
from django.urls import path, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages

from rest_framework import status
from django_admin_inline_paginator.admin import TabularInlinePaginated
from adminfilters.combo import RelatedFieldComboFilter, AllValuesComboFilter
from rangefilter.filters import NumericRangeFilter

from apps.anime.models import (
    Anime, Episode, Director, Studio, PreviewImage, Voiceover, VoiceoverHistory, Poster, Genre, Arch
)
from apps.core.admin import OnlyAddPermissionMixin, ReadOnlyPermissionsMixin, OnlyChangePermissionMixin
from apps.anime.choices import VoiceoverHistoryEvents
from apps.anime.forms import AnimeAdminForm
from apps.core.utils import get_instance_or_ajax_redirect
from apps.anime.admin_filters import AnimeFilter

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
    search_fields = ('first_name', 'last_name')
    search_help_text = 'Search by First name, Last name'
    list_display = ['first_name', 'last_name', 'url']
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


class RelatedAnimeAdmin(OnlyAddPermissionMixin, TabularInlinePaginated):
    model = Anime.related.through
    fk_name = 'from_anime'
    extra = 0


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    form = AnimeAdminForm
    search_fields = ('title', )
    search_help_text = 'Search by Title'
    list_display = ['display_poster', 'title', 'display_count_episodes', 'display_type',
                    'display_season', 'year']
    inlines = [EpisodeTabularInlinePaginated, PreviewImageTabularInlinePaginated, RelatedAnimeAdmin]
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
    readonly_fields = ['slug']
    exclude = ['related']

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
        return obj.episode_set.count()

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

    autocomplete_fields = ('anime',)

    list_filter = [
        AnimeFilter,
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
    list_display = ['display_anime', 'episode', 'team', 'user', 'type', 'status']
    inlines = [VoiceoverHistoryInline]

    fields = ('episode', 'team', 'type', 'file')
    autocomplete_fields = ('episode',)

    list_filter = [
        ('team', RelatedFieldComboFilter),
        ('type', AllValuesComboFilter),
        ('status', AllValuesComboFilter),
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
            'admin/js/utils/confirm_modal.js',
        )

    def add_view(self, request, form_url="", extra_context=None):
        self.readonly_fields = ()
        return super().add_view(request, form_url, extra_context)

    def edit_view(self, request, object_id, *args, **kwargs):
        """
        edit_view created for editing objects created via admin,
        change_view used for viewing objects
        """
        self.readonly_fields = ('episode', 'team', 'type')
        return super().change_view(
            request, object_id, extra_context={'edit': True, 'show_delete': False}, *args, **kwargs
        )

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context.update({
            'user_has_change_permission': request.user.has_perm('anime.change_voiceover')
        })
        self.readonly_fields = ('episode', 'team', 'type', 'file')
        return super(VoiceoverAdmin, self).change_view(request, object_id, form_url, extra_context)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('episode__anime', 'episode', 'team', 'user')

    @admin.display()
    def display_anime(self, obj: Voiceover):
        return obj.episode.anime.title

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('<str:object_id>/add-note/',
                 self.admin_site.admin_view(self.add_note),
                 name='voiceover_add_note'),
            path('<str:object_id>/decline/',
                 self.admin_site.admin_view(self.decline),
                 name='voiceover_decline'),
            path('<str:object_id>/approve/',
                 self.admin_site.admin_view(self.approve),
                 name='voiceover_approve'),
            path('<str:object_id>/edit/',
                 self.admin_site.admin_view(self.edit_view),
                 name='edit_voiceover'),
        ]
        return my_urls + urls

    @method_decorator(require_POST)
    @get_instance_or_ajax_redirect(error_message="Voiceover does not exist!",
                                   redirect_url='admin:anime_voiceover_changelist')
    def decline(self, request, object_id, instance: Voiceover):
        instance.process_new_history_event(
            event=VoiceoverHistoryEvents.DECLINED,
            user=request.user,
        )
        self.message_user(request, "The Voiceover has been successfully decline!",
                          level=messages.SUCCESS)
        return JsonResponse(data={
            'redirectUrl': reverse('admin:anime_voiceover_change', args=(instance.id,))
        })

    @method_decorator(require_POST)
    @get_instance_or_ajax_redirect(error_message="Voiceover does not exist!",
                                   redirect_url='admin:anime_voiceover_changelist')
    def approve(self, request, object_id, instance: Voiceover):
        instance.process_new_history_event(
            event=VoiceoverHistoryEvents.APPROVED,
            user=request.user,
        )
        self.message_user(request, "The Voiceover has been successfully approve!", level=messages.SUCCESS)
        return JsonResponse(data={
            'redirectUrl': reverse('admin:anime_voiceover_change', args=(instance.id,))
        })

    @method_decorator(require_POST)
    @get_instance_or_ajax_redirect(error_message="Voiceover does not exist!",
                                   redirect_url='admin:anime_voiceover_changelist')
    def add_note(self, request, object_id, instance: Voiceover):
        if request.POST.get('userComment', '') == '':
            return JsonResponse(data={}, status=status.HTTP_400_BAD_REQUEST)

        instance.process_new_history_event(
            event=VoiceoverHistoryEvents.COMMENT,
            user=request.user,
            message=request.POST['userComment'],
        )

        self.message_user(request, "The comment has been successfully added!", level=messages.SUCCESS)
        return JsonResponse(data={
            'redirectUrl': reverse('admin:anime_voiceover_change', args=(instance.id,))
        })

    def save_model(self, request, obj, form, change):
        obj.user = request.user
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
            obj.process_new_history_event(
                event=VoiceoverHistoryEvents.WAIT,
                created=timezone.now()
            )


class TOP100(Anime):
    class Meta:
        proxy = True
        verbose_name = 'Top 100'
        verbose_name_plural = 'Top 100'


@admin.register(TOP100)
class TOP100Admin(OnlyChangePermissionMixin, admin.ModelAdmin):
    list_filter = (
        AnimeFilter,
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_top=True)


@admin.register(Poster)
class PosterAdmin(admin.ModelAdmin):
    list_display = ['anime', 'display_poster', 'created']
    list_filter = (
        AnimeFilter,
    )

    @admin.display(description='Poster')
    def display_poster(self, obj: Poster):
        if not obj.image:
            return self.get_empty_value_display()
        return format_html(
            '<img style="height: 100px; width: 50px;" src="{url}">',
            url=obj.image.url
        )


@admin.register(Arch)
class ArchAdmin(admin.ModelAdmin):
    list_display = ['title', 'anime']
    list_filter = (
        AnimeFilter,
    )

    inlines = [EpisodeTabularInlinePaginated]
