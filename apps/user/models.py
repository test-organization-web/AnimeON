from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager


class User(PermissionsMixin, AbstractBaseUser):
    objects = UserManager()
    email = models.EmailField(unique=True, blank=True)
