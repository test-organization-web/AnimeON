from random import choice
from string import ascii_lowercase

from django.db import models


class CommentQuerySet(models.QuerySet):

    def filter_parents(self):
        return self.filter(parent__isnull=True)

    def filter_updated(self):
        return self.filter(updated__gt=models.F('created'))

    def filter_not_updated(self):
        return self.filter(updated=models.F('created'))

    def order_newest(self):
        return self.order_by('-created')

    def order_pinned_newest(self):
        return self.order_by('-is_pinned', '-created')

    def order_oldest(self):
        return self.order_by('created')

    def order_pinned_oldest(self):
        return self.order_by('-is_pinned', 'created')

    @staticmethod
    def generate_urlhash():
        return ''.join(choice(ascii_lowercase) for _ in range(8))


class ReactionQuerySet(models.QuerySet):
    def get_users(self):
        return [reaction.user for reaction in self.all()]