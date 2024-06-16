from django.db import models
from django.conf import settings
from apps.user.choices import UserAnimeChoices


class UserAnimeManager(models.Manager):
    def favorite(self, user: settings.AUTH_USER_MODEL):
        return self.filter(user=user, action=UserAnimeChoices.FAVORITE)

    def viewed(self, user: settings.AUTH_USER_MODEL):
        return self.filter(user=user, action=UserAnimeChoices.VIEWED)

    def dropped(self, user: settings.AUTH_USER_MODEL):
        return self.filter(user=user, action=UserAnimeChoices.DROPPED)

    def planned(self, user: settings.AUTH_USER_MODEL):
        return self.filter(user=user, action=UserAnimeChoices.PLANNED)

    def watching(self, user: settings.AUTH_USER_MODEL):
        return self.filter(user=user, action=UserAnimeChoices.WATCHING)
