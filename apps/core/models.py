from django.db import models

# Create your models here.


class CreatedDateTimeMixin(models.Model):
    created = models.DateTimeField('Created date and time', auto_now_add=True)

    class Meta:
        abstract = True


class UpdatedDateTimeMixin(models.Model):
    updated = models.DateTimeField('Updated date and time', auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class OrderMixin(models.Model):
    order = models.SmallIntegerField()

    class Meta:
        abstract = True


class VerifyMixin(models.Model):
    verified = models.BooleanField('Verified', default=False)

    class Meta:
        abstract = True

    def set_verified(self, save=True):
        self.verified = True
        if save:
            self.save()
