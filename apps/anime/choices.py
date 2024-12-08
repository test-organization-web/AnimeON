from django.db import models
from django.conf import settings


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
    WAIT = 'WAIT', 'Чекає на підтвердження'
    CHANGED = 'CHANGED', 'Змінено'
    DECLINED = 'DECLINED', 'Відхилено'
    APPROVED = 'APPROVED', 'Підтвержено'
    COMMENT = 'COMMENT'


class RatingTypes(models.TextChoices):
    G = 'G', 'All Ages'
    PG = 'PG', 'Children'
    PG13 = 'PG13', 'Teens 13 and Older'
    R = 'R', '(violence & profanity)'
    RPLUS = 'RPLUS', 'Profanity & Mild Nudity'


class SeasonTypes(models.TextChoices):
    WINTER = 'WINTER', 'Зима'
    SPRING = 'SPRING', 'Весна'
    SUMMER = 'SUMMER', 'Літо'
    FALL = 'FALL', 'Осінь'


class DayOfWeekChoices(models.TextChoices):
    MONDAY = 'MONDAY', 'Понеділок'
    TUESDAY = 'TUESDAY', 'Вівторок'
    WEDNESDAY = 'WEDNESDAY', 'Середа'
    THURSDAY = 'THURSDAY', 'Четверг'
    FRIDAY = 'FRIDAY', 'П\'ятниця'
    SATURDAY = 'SATURDAY', 'Субота'
    SUNDAY = 'SUNDAY', 'Неділя'


class ReactionChoices(models.TextChoices):
    LIKE = 'LIKE'
    DISLIKE = 'DISLIKE'


class AnimeHistoryEvents(models.TextChoices):
    SET_TOP = 'SET_TOP', 'Додано в ТОП'
    RESET_TOP = 'RESET_TOP', 'Видалено з ТОП'
