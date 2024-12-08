from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django_admin_inline_paginator.admin import TabularInlinePaginated
from django.contrib.auth import get_user_model

from apps.user.models import Group as CustomGroup, UserSettings, GroupSettings

UserModel = get_user_model()


admin.site.unregister(Group)


class UserTabularInlinePaginated(TabularInlinePaginated):
    model = UserModel.groups.through
    autocomplete_fields = ('user',)


class UserSettingsInlinePaginated(TabularInlinePaginated):
    model = UserSettings


class GroupSettingsInlinePaginated(TabularInlinePaginated):
    model = GroupSettings


@admin.register(CustomGroup)
class CustomGroupAdmin(admin.ModelAdmin):
    inlines = [GroupSettingsInlinePaginated, UserTabularInlinePaginated]
    pass


@admin.register(UserModel)
class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            "fields": ("username", "email", "password1", "password2"),
        }),
    )

    inlines = [UserSettingsInlinePaginated]

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(request, queryset, search_term)
        queryset = queryset.filter(is_staff=True)
        return queryset, may_have_duplicates
