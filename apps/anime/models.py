from django.db import models
from django.conf import settings
from django_countries.fields import CountryField

from apps.core.models import CreatedDateTimeMixin, UpdatedDateTimeMixin, VerifyMixin, OrderMixin
from apps.anime.choices import (
    VoiceoverTypes, AnimeTypes, RatingTypes, SeasonTypes, VoiceoverStatuses, VoiceoverHistoryEvents,
    AnimeStatuses, DayOfWeekChoices, ReactionChoices
)
from apps.anime.managers import AnimeManager, ReactionQuerySet
from apps.anime.s3_path import (
    anime_preview_image_save_path, anime_background_image_save_path, anime_poster_image_save_path,
    anime_card_image_save_path, episode_preview_image_save_path,
)
from apps.user.models import Group

# Create your models here.


class Director(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Studio(CreatedDateTimeMixin, models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(default='', blank=True)

    def __str__(self):
        return f'{self.name}'


class PreviewImage(models.Model):
    anime = models.ForeignKey('anime.Anime', on_delete=models.CASCADE)
    file = models.ImageField(upload_to=anime_preview_image_save_path, null=True)


class Anime(CreatedDateTimeMixin, UpdatedDateTimeMixin, models.Model):
    title = models.CharField(max_length=255, default='', db_index=True)
    type = models.CharField(max_length=255, choices=AnimeTypes.choices)
    slug = models.SlugField(max_length=255, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=255, choices=AnimeStatuses.choices, default=AnimeStatuses.ANNOUNCED)
    studio = models.ManyToManyField('anime.Studio', blank=True)
    rating = models.CharField(max_length=255, choices=RatingTypes.choices)
    related = models.ManyToManyField('self', blank=True)
    description = models.TextField(blank=True, default='')
    other_title = models.CharField(max_length=255, default='')
    genres = models.ManyToManyField('anime.Genre', blank=True)
    director = models.ForeignKey('anime.Director', null=True, on_delete=models.SET_NULL)
    season = models.CharField(max_length=255, choices=SeasonTypes.choices, default=SeasonTypes.SUMMER)
    is_top = models.BooleanField(default=False)
    background_image = models.ImageField(upload_to=anime_background_image_save_path, null=True)
    card_image = models.ImageField(upload_to=anime_card_image_save_path, null=True)
    year = models.PositiveSmallIntegerField()
    average_time_episode = models.PositiveSmallIntegerField(help_text='in minutes', null=True, blank=True)
    release_day_of_week = models.CharField(choices=DayOfWeekChoices.choices, null=True, blank=True)
    country = CountryField(null=True, blank=True)
    trailer_url = models.URLField(null=True, blank=True)

    objects = AnimeManager()

    def __str__(self):
        return f'{self.title}'

    def clean(self):
        super().clean()
        self.slug = self.__class__.objects.normalize_slug(self.title)

    def get_distinct_team(self):
        return Group.objects.prefetch_related('voiceover_set__episode').filter(
            voiceover__episode__in=self.episode_set.all()
        ).distinct()

    def get_similar(self):
        return Anime.objects.prefetch_related('genres').filter(
            genres__in=self.genres.all()
        )[:6]

    def get_count_by_reaction(self, reaction: ReactionChoices.values) -> int:
        return self.reactions.filter(reaction=reaction).count()


class Reaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='anime_reactions', on_delete=models.CASCADE,
                             editable=False)
    anime = models.ForeignKey('Anime', related_name='reactions', on_delete=models.CASCADE, editable=False)
    reaction = models.CharField(choices=ReactionChoices.choices, default='')

    objects = ReactionQuerySet.as_manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'anime'], name='unique_%(app_label)s_%(class)s_user_reaction'
            )
        ]

    def __str__(self):
        return f'{self.user} <{self.reaction}> ({self.anime.title})'


class Episode(CreatedDateTimeMixin, UpdatedDateTimeMixin, OrderMixin, models.Model):
    title = models.CharField(max_length=255)
    anime = models.ForeignKey('anime.Anime', on_delete=models.CASCADE)
    release_date = models.DateField(null=True)
    status = models.CharField(max_length=255)
    arch = models.ForeignKey('anime.Arch', on_delete=models.SET_NULL, null=True, blank=True)
    is_accessible = models.BooleanField(default=False)
    start_opening = models.PositiveSmallIntegerField(help_text='in seconds', null=True, blank=True)
    end_opening = models.PositiveSmallIntegerField(help_text='in seconds', null=True, blank=True)
    start_ending = models.PositiveSmallIntegerField(help_text='in seconds', null=True, blank=True)
    end_ending = models.PositiveSmallIntegerField(help_text='in seconds', null=True, blank=True)
    preview_image = models.ImageField(upload_to=episode_preview_image_save_path, null=True, blank=True)

    class Meta:
        ordering = ['-order']
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'anime'], name='unique_episode_for_anime'
            )
        ]

    def __str__(self):
        return f'ep#{self.order} {self.title}'

    @property
    def voiceovers(self):
        return self.voiceover_set.filter(type=VoiceoverTypes.VOICEOVER)

    @property
    def subtitles(self):
        return self.voiceover_set.filter(type=VoiceoverTypes.SUBTITLES)


class Arch(OrderMixin, models.Model):
    title = models.CharField(max_length=255)
    anime = models.ForeignKey('anime.Anime', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'anime'], name='unique_arch_for_anime'
            )
        ]

    def __str__(self):
        return f'{self.title}'


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.name}'


class Voiceover(CreatedDateTimeMixin, UpdatedDateTimeMixin, models.Model):
    type = models.CharField(max_length=255, choices=VoiceoverTypes.choices)
    episode = models.ForeignKey('anime.Episode', on_delete=models.CASCADE)
    team = models.ForeignKey('user.Group', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    status = models.CharField(choices=VoiceoverStatuses.choices, max_length=255)
    url = models.URLField()

    def __str__(self):
        return f'voiceover# {self.episode.title} ({self.team.name})'

    def is_can_be_approved(self, user: settings.AUTH_USER_MODEL):
        return self.user != user

    def process_new_history_event(self, event: VoiceoverHistoryEvents, **kwargs) -> 'VoiceoverHistory':
        old_status = self.status

        history_record = self.voiceover_history.create(event=event, **kwargs)
        self.revaluate_status()

        if self.status != old_status:
            history_record.status = self.status
            history_record.save(update_fields=['status'])

        return history_record

    def revaluate_status(self):
        """
        Note: should be called AFTER the voiceover history has been created
        """

        history = self.voiceover_history

        if history.filter(event=VoiceoverHistoryEvents.DECLINED).exists():
            new_status = VoiceoverStatuses.DECLINED
        elif history.filter(event=VoiceoverHistoryEvents.APPROVED).exists():
            new_status = VoiceoverStatuses.APPROVED
        elif history.filter(event=VoiceoverHistoryEvents.WAIT).exists():
            new_status = VoiceoverStatuses.WAIT
        else:
            new_status = VoiceoverStatuses.CREATED

        if self.status != new_status:
            self.status = new_status
            self.save(update_fields=["status"])


class VoiceoverHistory(CreatedDateTimeMixin, models.Model):
    voiceover = models.ForeignKey('Voiceover', on_delete=models.CASCADE, related_name='voiceover_history')
    message = models.CharField(max_length=255, blank=True)
    event = models.CharField(max_length=50, choices=VoiceoverHistoryEvents.choices)
    status = models.CharField(max_length=100, blank=True, choices=VoiceoverStatuses.choices)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Voiceover history'
        verbose_name_plural = 'Voiceover history'
        indexes = [
            models.Index(fields=['event', 'voiceover_id'])
        ]


class Poster(CreatedDateTimeMixin, models.Model):
    anime = models.OneToOneField('anime.Anime', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=anime_poster_image_save_path, null=True)
    description = models.TextField(blank=True, default='')
