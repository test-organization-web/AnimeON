from django.utils import timezone

from apps.core.utils import get_extension


def anime_preview_image_save_path(instance, filename: str):
    name = filename.split('.')[0]
    extension = get_extension(filename) or 'jpeg'
    path = f'{instance.anime.id}/preview/{name}.{extension}'
    return timezone.now().strftime(path)


def anime_background_image_save_path(instance, filename: str):
    name = filename.split('.')[0]
    extension = get_extension(filename) or 'jpeg'
    path = f'{instance.id}/background/{name}.{extension}'
    return timezone.now().strftime(path)


def anime_card_image_save_path(instance, filename: str):
    name = filename.split('.')[0]
    extension = get_extension(filename) or 'jpeg'
    path = f'{instance.id}/card/{name}.{extension}'
    return timezone.now().strftime(path)


def episode_preview_image_save_path(instance, filename: str):
    name = filename.split('.')[0]
    extension = get_extension(filename) or 'jpeg'
    path = f'{instance.id}/preview/{name}.{extension}'
    return timezone.now().strftime(path)


def anime_poster_image_save_path(instance, filename: str):
    name = filename.split('.')[0]
    extension = get_extension(filename) or 'jpeg'
    path = f'{instance.anime.id}/poster/{name}.{extension}'
    return timezone.now().strftime(path)