from django.db import models


class GeneralEvents(models.TextChoices):
    ASSIGNED = 'ASSIGNED', 'Тікет був пизначений'
    UNASSIGNED = 'UNASSIGNED', 'Тікет позбувся пизначення'
    IN_PROGRESS = 'IN_PROGRESS', 'Тікет в процесі'
    RESOLVED = 'RESOLVED', 'Тікет був вирішений'
    OPEN = 'OPEN', 'Тікет відкритий'
    COMMENT = 'COMMENT'


class RightholderAppealStatus(models.TextChoices):
    OPEN = 'OPEN'
    IN_PROGRESS = 'IN_PROGRESS'
    RESOLVED = 'RESOLVED'


class RightholderAppealEvents(models.TextChoices):
    ASSIGNED = 'ASSIGNED', 'Тікет був пизначений'
    UNASSIGNED = 'UNASSIGNED', 'Тікет позбувся пизначення'
    IN_PROGRESS = 'IN_PROGRESS', 'Тікет в процесі'
    RESOLVED = 'RESOLVED', 'Тікет був вирішений'
    OPEN = 'OPEN', 'Тікет відкритий'
    COMMENT = 'COMMENT'


class HelpAppealStatus(models.TextChoices):
    OPEN = 'OPEN'
    IN_PROGRESS = 'IN_PROGRESS'
    RESOLVED = 'RESOLVED'


class HelpAppealEvents(models.TextChoices):
    ASSIGNED = 'ASSIGNED', 'Тікет був пизначений'
    UNASSIGNED = 'UNASSIGNED', 'Тікет позбувся пизначення'
    IN_PROGRESS = 'IN_PROGRESS', 'Тікет в процесі'
    RESOLVED = 'RESOLVED', 'Тікет був вирішений'
    OPEN = 'OPEN', 'Тікет відкритий'
    COMMENT = 'COMMENT'
