from django.core.cache import cache
from django.http import JsonResponse

from rest_framework import status

from apps.core.utils import get_client_ip, get_response_body_errors


IPSpanCacheKey = 'spam.{spam_key}.ip.{ip}'

spam_timeout = 30


class CheckIPSpam:
    spam_key: str

    def dispatch(self, request, *args, **kwargs):
        ip = get_client_ip(request)
        cache_key = IPSpanCacheKey.format(spam_key=self.spam_key, ip=ip)
        has_spam = cache.get(cache_key)
        if has_spam:
            response_data = get_response_body_errors(errors=f'Спробуйте повторити запит через {spam_timeout} секунд')
            return JsonResponse(data=response_data, status=status.HTTP_403_FORBIDDEN)
        cache.set(cache_key, True, timeout=spam_timeout)
        return super().dispatch(request, *args, **kwargs)
