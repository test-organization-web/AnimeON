from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.models import Group as BaseGroup
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.db import models
from django.conf import settings

from apps.user.choices import UserAnimeChoices
from apps.user.s3_path import user_avatar_save_path, group_avatar_save_path


class User(PermissionsMixin, AbstractBaseUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': "Користувач з таким username вже існує",
        },
    )
    first_name = models.CharField("first name", max_length=150, blank=True)
    last_name = models.CharField("last name", max_length=150, blank=True)
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    email = models.EmailField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text='Designates whether this user should be treated as active. '
                  'Unselect this instead of deleting accounts.',
    )
    date_joined = models.DateTimeField('date joined', default=timezone.now)
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_count_viewed_anime(self):
        return self.useranime_set.filter(action=UserAnimeChoices.VIEWED).count()

    def get_count_commented_anime(self):
        return self.comments.count()


class UserSettings(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='settings', to_field='username'
    )
    avatar = models.ImageField(blank=True, null=True, upload_to=user_avatar_save_path)
    telegram = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return f'{self.user} settings'


class GroupSettings(models.Model):
    group = models.OneToOneField(
        BaseGroup, on_delete=models.CASCADE, related_name='settings'
    )
    avatar = models.ImageField(blank=True, null=True, upload_to=group_avatar_save_path)

    def __str__(self):
        return f'{self.group} settings'


class Group(BaseGroup):
    class Meta:
        proxy = True
        verbose_name = 'Group'
        verbose_name_plural = "Groups"


class UserAnime(models.Model):
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    anime = models.ForeignKey('anime.Anime', on_delete=models.CASCADE)
    action = models.CharField(choices=UserAnimeChoices.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'action', 'anime'], name='unique_%(app_label)s_%(class)s_user_anime_action'
            )
        ]


class UserEpisodeViewed(models.Model):
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='viewed_episode')
    episode = models.ForeignKey('anime.Episode', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'episode'], name='unique_%(app_label)s_%(class)s_user_episode'
            )
        ]
