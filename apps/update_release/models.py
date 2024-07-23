from django.db import models
from django.conf import settings
from django.utils import timezone

from apps.core.models import CreatedDateTimeMixin, UpdatedDateTimeMixin
from apps.update_release.choices import UpdateReleaseSources
from apps.update_release.managers import MyAnimeListTokenManager

# Create your models here.


class UpdateRelease(CreatedDateTimeMixin, models.Model):
    source = models.CharField(choices=UpdateReleaseSources.choices)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    content = models.JSONField(default=dict)


class MyAnimeListToken(CreatedDateTimeMixin, UpdatedDateTimeMixin, models.Model):
    refresh_token = models.TextField(default='')
    access_token = models.TextField(default='')
    code_verifier = models.TextField(default='')
    code_challenge = models.TextField(default='')
    authorisation_url = models.URLField(default='', max_length=500)
    expires_in = models.PositiveIntegerField(default=0)
    expired_date = models.DateTimeField(default=timezone.now)
    token_type = models.CharField(default='', max_length=255)

    objects = MyAnimeListTokenManager()

    def clean(self):
        super().clean()
        self.expired_date = self.__class__.objects.get_expired_date(self.expires_in)
        print("HHRERERERERER")
        print(self.expired_date)


