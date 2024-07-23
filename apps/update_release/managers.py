from django.db import models
from django.utils import timezone
from datetime import timedelta


class MyAnimeListTokenManager(models.Manager):

    @staticmethod
    def get_expired_date(expires_in):
        return timezone.now() + timedelta(seconds=expires_in)

    def get_active(self):
        return self.get_queryset().filter(
            expired_date__gt=timezone.now()
        ).first()
