from django.db import models
from django.db.models import Count

from slugify import slugify


class AnimeManager(models.Manager):
    @classmethod
    def normalize_slug(cls, title):
        """
        Normalize the slug by lowercasing.
        """
        title = title or ""
        return slugify(title.strip())

    def get_queryset(self):
        return super().get_queryset().annotate(
            count_episodes=Count('episode')
        )


class ReactionQuerySet(models.QuerySet):
    def get_users(self):
        return [reaction.user for reaction in self.all()]
