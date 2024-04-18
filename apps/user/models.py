from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.models import Group as BaseGroup
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone


class User(PermissionsMixin, AbstractBaseUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    first_name = models.CharField("first name", max_length=150, blank=True)
    last_name = models.CharField("last name", max_length=150, blank=True)
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    email = models.EmailField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text='Designates whether this user should be treated as active. '
                  'Unselect this instead of deleting accounts.',
    )
    date_joined = models.DateTimeField('date joined', default=timezone.now)
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


class Group(BaseGroup):

    class Meta:
        proxy = True
        verbose_name = 'Group'
        verbose_name_plural = "Groups"
