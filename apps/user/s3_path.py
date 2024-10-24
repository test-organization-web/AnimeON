from django.utils import timezone

from apps.core.utils import get_extension


def user_avatar_save_path(instance, filename: str):
    name = filename.split('.')[0]
    extension = get_extension(filename) or 'jpeg'
    path = f'users/{instance.user.username}/avatar/{name}.{extension}'
    return timezone.now().strftime(path)