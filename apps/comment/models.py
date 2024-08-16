from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings

from apps.core.models import CreatedDateTimeMixin
from apps.comment.managers import CommentQuerySet, ReactionQuerySet
from apps.comment.choices import ReactionChoices


class Comment(CreatedDateTimeMixin, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content_main = models.TextField()
    content = models.TextField()  # edited content will store here
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reply', null=True, blank=True)
    is_spoiler = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    urlhash = models.CharField(max_length=50, unique=True, editable=False)
    updated = models.DateTimeField(auto_now=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = CommentQuerySet.as_manager()

    class Meta:
        ordering = ('-is_pinned', '-created')

    def __str__(self):
        if not self.parent:
            return f'{self.content_main[:20]}'
        else:
            return f'[RE] ({self.parent.content_main[:10]}) : {self.content_main[:15]}'

    def set_unique_urlhash(self):
        if not self.urlhash:
            self.urlhash = self.__class__.objects.generate_urlhash()
            while self.__class__.objects.filter(urlhash=self.urlhash).exists():
                self.urlhash = self.__class__.objects.generate_urlhash()

    def save(self, *args, **kwargs):
        self.set_unique_urlhash()
        super().save(*args, **kwargs)

    def has_reply(self) -> bool:
        return self.reply.all().exists()

    def get_count_like(self) -> int:
        return self.reactions.filter(reaction=ReactionChoices.LIKE).count()

    def get_count_dislike(self) -> int:
        return self.reactions.filter(reaction=ReactionChoices.DISLIKE).count()

    @property
    def is_parent(self):
        return self.parent is None


class Reaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comment_reactions', on_delete=models.CASCADE,
                             editable=False)
    comment = models.ForeignKey(Comment, related_name='reactions', on_delete=models.CASCADE, editable=False)
    reaction = models.CharField(choices=ReactionChoices.choices, default='')

    objects = ReactionQuerySet.as_manager()

    class Meta:
        unique_together = ['user', 'comment']

    def __str__(self):
        return f'{self.user} <{self.reaction}> ({self.comment.content_main[:20]})'
