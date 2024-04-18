from django.db import models


class AnimeStatuses(models.TextChoices):
    CAME_OUT = 'CAME_OUT', 'Вийшов'
    COMES_OUT = 'COMES_OUT', 'Виходить'
    ANNOUNCED = 'ANNOUNCED', 'Анонсовано'


class AnimeTypes(models.TextChoices):
    ANIME = 'ANIME', 'Аніме'
    FILM = 'FILM', 'Фільм'


class VoiceoverTypes(models.TextChoices):
    VOICEOVER = 'VOICEOVER', 'Озвучка'
    SUBTITLES = 'SUBTITLES', 'Субтитри'


class VoiceoverStatuses(models.TextChoices):
    CREATED = 'CREATED', 'CREATED'
    WAIT = 'WAIT', 'WAIT'
    DECLINED = 'DECLINED', 'DECLINED'
    APPROVED = 'APPROVED', 'APPROVED'


class VoiceoverHistoryEvents(models.TextChoices):
    pass


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
