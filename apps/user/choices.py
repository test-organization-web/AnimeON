from django.db import models


class UserAnimeChoices(models.TextChoices):
    FAVORITE = 'FAVORITE'
    VIEWED = 'VIEWED'
    DROPPED = 'DROPPED'
    PLANNED = 'PLANNED'
    WATCHING = 'WATCHING'
