from django.core.management.base import BaseCommand

from django.db import transaction

from apps.anime.models import Genre, Director, Studio, Anime, Episode, Poster, Arch


class Command(BaseCommand):
    help = 'Delete all Anime and related objects'

    @transaction.atomic
    def handle(self, *args, **options):
        Anime.objects.all().delete()
        Director.objects.all().delete()
        Studio.objects.all().delete()
        Episode.objects.all().delete()
        Poster.objects.all().delete()
        Genre.objects.all().delete()
        Arch.objects.all().delete()
