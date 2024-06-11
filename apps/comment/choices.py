from django.db import models


class ReactionChoices(models.TextChoices):
    LIKE = 'LIKE'
    DISLIKE = 'DISLIKE'
