from django.contrib import admin, messages
from django.urls import path, reverse
from django.http import JsonResponse
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.utils import timezone

from anime_on.awscli import schedule_command
from apps.update_release.models import UpdateRelease
from apps.update_release.services.myanimelist.client import Client

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
        client = Client(
            client_id=settings.MYAL_CLIENT_ID,
            client_secret=settings.MYAL_CLIENT_SECRET
        )
        auth = client.auth()

        if auth['type'] == 'token':
            schedule_command(
                command='myanimelist_update_releases',
                start_time=timezone.now(),
                kwargs={'authorisation_code': auth['token']}
            )
            messages.info(
                request,
                'Команда оновлення релізів запущена, процедура займе деякий час. Оновіть сторінку пізніше'
            )
        elif auth['type'] == 'url':
            return JsonResponse(data={
                'redirectUrl': auth['url']
            })
        return JsonResponse(data={
            'redirectUrl': reverse('admin:update_release_updaterelease_changelist')
        })
