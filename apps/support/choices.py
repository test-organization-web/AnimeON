from django.db import models


class GeneralEvents(models.TextChoices):
    CREATED = 'CREATED', 'Тікет був створений'
    ASSIGNED = 'ASSIGNED', 'Тікет був пизначений'
    UNASSIGNED = 'UNASSIGNED', 'Тікет позбувся пизначений'
    IN_PROGRESS = 'IN_PROGRESS', 'Тікет в процесі'
    RESOLVED = 'RESOLVED', 'Тікет був вирішений'
    OPEN = 'OPEN', 'Тікет відкритий'
    COMMENT = 'COMMENT'


class RightholderAppealStatus(models.TextChoices):
    CREATED = 'CREATED'
    OPEN = 'OPEN'
    IN_PROGRESS = 'IN_PROGRESS'
    RESOLVED = 'RESOLVED'


class RightholderAppealEvents(models.TextChoices):
    CREATED = 'CREATED', 'Тікет був створений'
    ASSIGNED = 'ASSIGNED', 'Тікет був пизначений'
    UNASSIGNED = 'UNASSIGNED', 'Тікет позбувся пизначений'
    IN_PROGRESS = 'IN_PROGRESS', 'Тікет в процесі'
    RESOLVED = 'RESOLVED', 'Тікет був вирішений'
    OPEN = 'OPEN', 'Тікет відкритий'
    COMMENT = 'COMMENT'


class HelpAppealStatus(models.TextChoices):
    CREATED = 'CREATED'
    OPEN = 'OPEN'
    IN_PROGRESS = 'IN_PROGRESS'
    RESOLVED = 'RESOLVED'


class HelpAppealEvents(models.TextChoices):
    CREATED = 'CREATED', 'Тікет був створений'
    ASSIGNED = 'ASSIGNED', 'Тікет був пизначений'
    UNASSIGNED = 'UNASSIGNED', 'Тікет позбувся пизначений'
    IN_PROGRESS = 'IN_PROGRESS', 'Тікет в процесі'
    RESOLVED = 'RESOLVED', 'Тікет був вирішений'
    OPEN = 'OPEN', 'Тікет відкритий'
    COMMENT = 'COMMENT'
