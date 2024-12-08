from django.conf import settings


class ManyTOPAnimeException(Exception):
    def __init__(self):
        super().__init__(f'На разі в розділі ТОП-{settings.COUNT_TOP_ANIME} вже є достатня кількість '
                         f'аніме, передевіться варіанти і замініть')