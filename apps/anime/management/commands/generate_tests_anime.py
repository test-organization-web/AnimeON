from django.core.management.base import BaseCommand
from django_countries import Countries

from faker import Faker

from django.db import transaction
from django.utils import timezone

from apps.anime.models import Genre, Director, Studio, Anime, Episode, Arch, Poster
from apps.anime.choices import RatingTypes, SeasonTypes

fake = Faker()


class Command(BaseCommand):
    help = 'Generate useable data and fill the tables'

    def add_arguments(self, parser):
        parser.add_argument('--genres', type=int, default=10, help='Number of genres')
        parser.add_argument('--directors', type=int, default=10, help='Number of directors')
        parser.add_argument('--studios', type=int, default=10, help='Number of studio')
        parser.add_argument('--anime', type=int, default=10, help='Number of animes')
        parser.add_argument('--arches', type=int, default=10, help='Number of arches')
        parser.add_argument('--episodes', type=int, default=10, help='Number of episodes')
        parser.add_argument('--posters', type=int, default=10, help='Number of posters')

    @transaction.atomic
    def handle(self, *args, **options):
        num_genres = options['genres']
        num_directors = options['directors']
        num_studios = options['studios']
        num_anime = options['anime']
        num_arches = options['arches']
        num_episodes = options['episodes']
        num_posters = options['posters']

        self.generate_genres(num_genres)
        self.generate_directors(num_directors)
        self.generate_studios(num_studios)
        self.generate_arches(num_arches)
        self.generate_episodes(num_episodes)

        self.generate_anime(num_anime)
        self.generate_posters(num_posters)

        self.stdout.write(self.style.SUCCESS('Script has been successfully finished!'))

    def generate_genres(self, num_genres):
        count_genres = 0
        for _ in range(num_genres):
            name = fake.sentence()

            obj, created = Genre.objects.get_or_create(name=name)
            if not created:
                count_genres += 1
        self.stdout.write(self.style.SUCCESS(
            f'Finish create Genres: {count_genres} new records,'))

    def generate_directors(self, num_directors):
        count_directors = 0
        for _ in range(num_directors):
            first_name = fake.random_element(elements=['Tom', 'Test', 'Best'])
            last_name = fake.random_element(elements=['Tom', 'Test', 'Best'])
            pseudonym = fake.random_element(elements=['Tom', 'Test', 'Best'])
            url = 'http://localhost:8000'

            Director.objects.create(
                first_name=first_name, last_name=last_name, pseudonym=pseudonym, url=url
            )
            count_directors += 1
        self.stdout.write(self.style.SUCCESS(
            f'Finish create Directors: {count_directors} new records,'))

    def generate_studios(self, num_studios):
        count_studios = 0
        for _ in range(num_studios):
            name = fake.sentence()
            country = fake.random_element(elements=Countries())

            if Studio.objects.filter(name=name).exists():
                continue

            Studio.objects.create(
                name=name, description='test', country=country
            )
            count_studios += 1
        self.stdout.write(self.style.SUCCESS(
            f'Finish create Studios: {count_studios} new records,'))

    def generate_arches(self, num_arches):
        count_arches = 0
        animes = Anime.objects.all()
        order = 0

        for _ in range(num_arches):
            title = fake.sentence()
            anime = fake.random_element(elements=animes)

            if arch := Arch.objects.filter(anime=anime, order=order).order_by('-order').first():
                order += arch.order
                continue

            Arch.objects.create(
                title=title,
                anime=anime,
                order=order
            )
            count_arches += 1
        self.stdout.write(self.style.SUCCESS(
            f'Finish create Arches: {count_arches} new records,'))

    def generate_episodes(self, num_episodes):
        count_episodes = 0
        animes = Anime.objects.all()
        release_date = timezone.now().date()
        order = 0

        for _ in range(num_episodes):
            title = fake.sentence()
            anime = fake.random_element(elements=animes)
            arches = list(anime.arch_set.all())
            arch = fake.random_element(elements=arches + [None])

            if episode := Episode.objects.filter(order=order, anime=anime).order_by('-order').first():
                order += episode.order
                continue

            Episode.objects.create(
                title=title,
                anime=anime,
                status='TEST',
                arch=arch,
                release_date=release_date,
                order=order
            )
            count_episodes += 1
        self.stdout.write(self.style.SUCCESS(
            f'Finish create Episodes: {count_episodes} new records,'))

    def generate_anime(self, num_anime) -> None:
        count_anime = 0
        anime_already_exists_in_db = 0
        genres = Genre.objects.all()
        directors = Director.objects.all()

        studios = Studio.objects.all()
        start_date = timezone.now().date()

        for _ in range(num_anime):
            title = fake.sentence()
            genre = fake.random_element(elements=genres)
            director = fake.random_element(elements=directors)
            studio = fake.random_element(elements=studios)

            try:
                anime = Anime.objects.create(
                    title=title,
                    slug=Anime.objects.normalize_slug(title),
                    start_date=start_date,
                    rating=fake.random_element(elements=[choice[0] for choice in RatingTypes.choices]),
                    studio=studio,
                    director=director,
                    description=fake.sentence(),
                    short_description=fake.sentence(),
                    season=fake.random_element(elements=[choice[0] for choice in SeasonTypes.choices]),
                    rank=100,
                    status='TEST'
                )
            except Exception as error:
                self.stdout.write(self.style.WARNING(error))
                anime_already_exists_in_db += 1
                continue
            anime.genres.add(genre)
            count_anime += 1

        self.stdout.write(self.style.SUCCESS(
            f'Finish create Anime: {count_anime} new records,'
            f' already exists - {anime_already_exists_in_db}'))

    def generate_posters(self, num_posters):
        count_posters = 0
        posters_already_exists_in_db = 0

        animes = Anime.objects.all()

        for _ in range(num_posters):
            anime = fake.random_element(elements=animes)

            poster, created = Poster.objects.get_or_create(
                anime=anime,
                description=fake.sentence()
            )
            if created:
                posters_already_exists_in_db += 1
                continue
            count_posters += 1

        self.stdout.write(self.style.SUCCESS(
            f'Finish create Anime: {count_posters} new records,'
            f' already exists - {posters_already_exists_in_db}'))
