from django.db import models


class UserAnimeChoices(models.TextChoices):
    FAVORITE = 'FAVORITE', 'Улюблені'
    VIEWED = 'VIEWED', 'Переглянуті'
    DROPPED = 'DROPPED', 'Кинуті'
    PLANNED = 'PLANNED', 'Заплановані'
    WATCHING = 'WATCHING', 'Дивлюся зараз'
