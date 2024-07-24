import logging

from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone

from anime_on.awscli import schedule_command


logger = logging.getLogger(__name__)


def callback(request):
    logger.info('Start callback Myanimelist', extra={
        'message_id': 'myanimelist_callbak_start'
    })
    if 'code' not in request.GET:
        logger.warning('Callback Myanimelist doe not have code params', extra={
            'message_id': 'myanimelist_callbak_code_does_not_exists',
        })
        messages.warning(
            request,
            'Невдалося отримати код авторизації від myanimelist'
        )
    else:
        logger.warning('Schedule command update myanimelist releases', extra={
            'message_id': 'myanimelist_callback_schedule_command',
        })
        schedule_command(
            command='myanimelist_update_releases',
            start_time=timezone.now(),
            kwargs={'authorisation_code': request.GET['code']}
        )
        messages.info(
            request,
            'Команда оновлення релізів запущена, процедура займе деякий час. Оновіть сторінку пізніше'
        )
    return redirect('admin:anime_anime_changelist')
