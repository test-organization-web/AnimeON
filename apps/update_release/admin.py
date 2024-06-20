from django.contrib import admin, messages
from django.urls import path, reverse
from django.core.management import call_command
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST

from apps.update_release.models import UpdateRelease
from apps.update_release.services.myanimelist.exceptions import TokenMissing

# Register your models here.


@admin.register(UpdateRelease)
class UpdateReleaseAdmin(admin.ModelAdmin):
    list_display = ['source', 'user']

    class Media:
        css = {
            'all': (
                "css/jquery-1-13-2-ui-min.css",
                'admin/css/utils/dialog.css',
            )
        }
        js = (
            'js/js-cookie-v3-0-1.min.js',
            "js/jquery-1-13-2-ui-min.js",
            "admin/js/utils/dialog.js",
        )

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('update/myanimelist/', self.admin_site.admin_view(self.update_myanimelist_release),
                 name='update-myanimelist-release')
        ]
        return my_urls + urls

    @method_decorator(require_POST)
    def update_myanimelist_release(self, request):
        try:
            call_command('myanimelist_auth')
        except TokenMissing as error:
            self.message_user(request, str(error), level=messages.ERROR)
        return JsonResponse(data={
            'redirectUrl': reverse('admin:update_release_updaterelease_changelist')
        })
