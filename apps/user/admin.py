from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django_admin_inline_paginator.admin import TabularInlinePaginated

from apps.user.models import User
from apps.user.models import Group as CustomGroup


admin.site.unregister(Group)


class UserTabularInlinePaginated(TabularInlinePaginated):
    model = User.groups.through


@admin.register(CustomGroup)
class CustomGroupAdmin(admin.ModelAdmin):
    inlines = [UserTabularInlinePaginated]
    pass


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            "fields": ("username", "email", "password1", "password2"),
        }),
    )
