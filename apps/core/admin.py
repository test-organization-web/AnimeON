from django.conf import settings
from django.contrib import admin


admin.site.site_header = f'AnimeON {settings.PROJECT_VERSION}'
admin.site.site_title = 'AnimeON'
admin.site.index_title = 'Administration'


class ReadOnlyPermissionsMixin:
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class OnlyChangePermissionMixin:
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class OnlyAddPermissionMixin:
    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
