from django.db import models

from slugify import slugify


class AnimeManager(models.Manager):
    @classmethod
    def normalize_slug(cls, title):
        """
        Normalize the slug by lowercasing.
        """
        title = title or ""
        return slugify(title.strip())
