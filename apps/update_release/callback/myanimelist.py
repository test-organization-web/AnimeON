import logging

from django.http import JsonResponse
from django.utils import timezone

from anime_on.awscli import schedule_command


logger = logging.getLogger(__name__)


def callback(request):
    logger.info('Start callback Myanimelist', extra={
        'message_id': 'myanimelist_callbak_start'
    })
    if 'code' not in request.GET:
        logger.info('Callback Myanimelist doe not have code params', extra={
            'message_id': 'myanimelist_callbak_start'
        })
        return JsonResponse(data={})
    schedule_command(
        command='myanimelist_update_releases',
        start_time=timezone.now(),
        kwargs={'authorisation_code': request.GET['code']}
    )
    return JsonResponse(data={})
