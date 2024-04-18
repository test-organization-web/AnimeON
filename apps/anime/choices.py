from django.db import models


class AnimeStatuses(models.TextChoices):
    CAME_OUT = 'CAME_OUT', 'Вийшов'
    COMES_OUT = 'COMES_OUT', 'Виходить'
    ANNOUNCED = 'ANNOUNCED', 'Анонсовано'


class AnimeTypes(models.TextChoices):
    SERIAL = 'SERIAL', 'Серіал'
    FILM = 'FILM', 'Фільм'
    ONA = 'ONA', 'ONA'
    OVA = 'OVA', 'OVA'


class VoiceoverTypes(models.TextChoices):
    VOICEOVER = 'VOICEOVER', 'Озвучка'
    SUBTITLES = 'SUBTITLES', 'Субтитри'


class VoiceoverStatuses(models.TextChoices):
    CREATED = 'CREATED', 'CREATED'
    WAIT = 'WAIT', 'WAIT'
    DECLINED = 'DECLINED', 'DECLINED'
    APPROVED = 'APPROVED', 'APPROVED'


class VoiceoverHistoryEvents(models.TextChoices):
    CREATED = 'CREATED', 'Створено запит на додавання озвучки'


class RatingTypes(models.TextChoices):
    G = 'G', 'All Ages'
    PG = 'PG', 'Children'
    PG13 = 'PG13', 'Teens 13 and Older'
    R = 'R', '(violence & profanity)'
    RPLUS = 'RPLUS', 'Profanity & Mild Nudity'
    RX = 'RX', 'Hentai'


class SeasonTypes(models.TextChoices):
    WINTER = 'WINTER', 'Зима'
    SPRING = 'SPRING', 'Весна'
    SUMMER = 'SUMMER', 'Літо'
    FALL = 'FALL', 'Осінь'
