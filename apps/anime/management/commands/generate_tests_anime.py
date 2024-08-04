from django.core.management.base import BaseCommand
from django_countries import Countries

from faker import Faker

from django.db import transaction
from django.utils import timezone

from apps.anime.models import Genre, Director, Studio, Anime, Episode, Poster
from apps.anime.choices import RatingTypes, SeasonTypes, AnimeStatuses, DayOfWeekChoices

fake = Faker()


class Command(BaseCommand):
    help = 'Generate useable data and fill the tables'

    def add_arguments(self, parser):
        parser.add_argument('--episodes', type=int, default=10, help='Number of episodes')
        parser.add_argument('--posters', type=int, default=10, help='Number of episodes')

    @transaction.atomic
    def handle(self, *args, **options):
        num_episodes = options['episodes']
        num_posters = options['posters']

        self.generate_genres()
        self.generate_directors()
        self.generate_studios()

        self.generate_anime()
        self.generate_posters(num_posters)

        self.generate_episodes(num_episodes)

        self.stdout.write(self.style.SUCCESS('Script has been successfully finished!'))

    def generate_genres(self):
        genres = ['Комедія', 'Триллер', 'Бойовик', 'Мелодрама', 'Фантастика']
        count_genres = 0
        for genre in genres:
            obj, created = Genre.objects.get_or_create(name=genre)
            if not created:
                count_genres += 1
        self.stdout.write(self.style.SUCCESS(
            f'Finish create Genres: {count_genres} new records,'))

    def generate_directors(self):
        director_first_names = ['Том', 'Фітч', 'Кайл', 'Мейв', 'Пол']
        director_last_names = ['Такер', 'Дізель', 'Джонсон', 'Борисенко', 'Філімон']
        count_directors = 0
        for _ in range(len(director_first_names)):
            first_name = fake.random_element(elements=director_first_names)
            last_name = fake.random_element(elements=director_last_names)
            url = 'http://localhost:8000'

            Director.objects.create(
                first_name=first_name, last_name=last_name, url=url
            )
            count_directors += 1
        self.stdout.write(self.style.SUCCESS(
            f'Finish create Directors: {count_directors} new records,'))

    def generate_studios(self):
        count_studios = 0
        studios = ['BulBul Media', 'Unimay Media', 'Lifecycle']
        for studio in studios:

            if Studio.objects.filter(name=studio).exists():
                continue

            Studio.objects.create(
                name=studio, description='test',
            )
            count_studios += 1
        self.stdout.write(self.style.SUCCESS(
            f'Finish create Studios: {count_studios} new records,'))

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

    def generate_anime(self) -> None:
        count_anime = 0
        anime_already_exists_in_db = 0
        genres = Genre.objects.all()
        directors = Director.objects.all()

        studios = Studio.objects.all()
        start_date = timezone.now().date()

        descr = "Людство всю його історію тягнуло до всього містичного та невідомого." \
                " Знання занапастить людство і це факт. Жага знань не знає меж." \
                " Щодня вчені прагнуть відкрити щось нове. Це принесе людству порятунок чи загибель." \
                " Не можна лізти туди, де великими літерами написано «УБ'Є». Однак, як ви всі знаєте," \
                " ми не можемо вгамувати свою жагу до цікавості і знань. Ми хочемо знати все." \
                " «Магічна Битва» покаже вам наочно, як проста спрага знань і помилка спричинили" \
                " великі неприємності для всього людства. Жага відкрити якийсь «предмет» із" \
                " захисними чарами випустила назовні сили, здатні поглинути у темряву весь світ." \
                " Здавалося б, з цією проблемою розібралися, але ніхто не міг припустити, що вона," \
                " проблема, повернеться з новою силою.У світі нашого Аніме відбуваються цікаві події." \
                " Люди можуть зникнути без будь-якої причини. Здавалося б, а куди вони поділися?" \
                " Відповідь криється в демонах, які прагнуть затягнути якнайбільше людей у ​​вир" \
                " темряви. Юдзі Ітадорі не пощастило народитися у такому світі. Головний герой" \
                " усіляко намагається уникати спортивних клубів. Він дуже сильний фізично. Не дивно," \
                " що його намагаються затягнути до клубів зі спортивною тематикою. Незважаючи на всі " \
                "їхні спроби, Юдзі вступає до клубу окультних наук. Тут щось усе і починається." \
                " Відкривши «Скриньку Пандори» і випустивши у світ невідані сили, Юдзі, потрібно" \
                " вижити і вирішити цю проблему. Відповідати за свої вчинки просто неодмінно." \
                " Щодня відвідувати в лікарні свого дідуся, вирішувати проблеми відкритого ящика…" \
                " Ось це я розумію життя школяра. Приємного перегляду!"

        short_descr = "Людство всю його історію тягнуло до всього містичного та невідомого." \
                      " Знання занапастить людство і це факт. Жага знань не знає меж."

        anime_names = ['Бліч', 'Наруто', 'Магічна Битва', 'Код Гіас', 'Кайдзю 8', 'Ван Піс',
                       'Тестостерон', 'Атака титанів', 'Кайдзю', 'ТораДора', 'Людина-бензопила',
                       'Хвіс Феї', 'Хелсінг', 'Я моряк', 'Моряк Папай', 'Скубі-ду', 'Мордок',
                       'Володар перстнів', 'Гаррі Поттер', 'Феї Вінкс']
        for title in anime_names:
            genre = fake.random_element(elements=genres)
            director = fake.random_element(elements=directors)
            studio = fake.random_element(elements=studios)

            try:
                anime = Anime.objects.create(
                    country=fake.random_element(elements=Countries()),
                    title=title,
                    slug=Anime.objects.normalize_slug(title),
                    start_date=start_date,
                    rating=fake.random_element(elements=[choice[0] for choice in RatingTypes.choices]),
                    director=director,
                    description=descr,
                    short_description=short_descr,
                    season=fake.random_element(elements=[choice[0] for choice in SeasonTypes.choices]),
                    rank=100,
                    status=fake.random_element(elements=[choice[0] for choice in AnimeStatuses.choices]),
                    year=fake.random_element(elements=[2020, 2021, 2022, 2023, 2024]),
                    release_day_of_week=fake.random_element(elements=[choice[0] for choice in DayOfWeekChoices.choices]),
                )
            except Exception as error:
                self.stdout.write(self.style.WARNING(error))
                anime_already_exists_in_db += 1
                continue
            anime.genres.add(genre)
            anime.studio.add(studio)
            count_anime += 1

        self.stdout.write(self.style.SUCCESS(
            f'Finish create Anime: {count_anime} new records,'
            f' already exists - {anime_already_exists_in_db}'))

    def generate_posters(self, num_posters):
        count_posters = 0
        posters_already_exists_in_db = 0

        animes = Anime.objects.all()

        descr = "Людство всю його історію тягнуло до всього містичного та невідомого." \
                " Знання занапастить людство і це факт. Жага знань не знає меж."

        for _ in range(num_posters):
            anime = fake.random_element(elements=animes)

            poster, created = Poster.objects.get_or_create(
                anime=anime,
                defaults=dict(
                    description=descr
                )
            )
            if created:
                posters_already_exists_in_db += 1
                continue
            count_posters += 1

        self.stdout.write(self.style.SUCCESS(
            f'Finish create Anime: {count_posters} new records,'
            f' already exists - {posters_already_exists_in_db}'))
