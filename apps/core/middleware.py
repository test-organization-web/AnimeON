import logging

from django.http import HttpResponse

from anime_on.logging import request_id_context
from uuid import uuid4


logger = logging.getLogger(__name__)


def request_id_middleware(get_response):
    def middleware(request):
        request_id = request.headers.get("X-Request-ID") or uuid4().hex
        with request_id_context(request_id):
            response = get_response(request)
        response.headers['X-Request-ID'] = request_id
        return response
    return middleware


def ping_middleware(get_response):
    def middleware(request):
        if request.META["PATH_INFO"] == "/ping/":
            return HttpResponse("pong")
        else:
            return get_response(request)
    return middleware


def error_logging_middleware(get_response):
    def middleware(request):
        request_body = request.body
        response = get_response(request)
        if 400 <= response.status_code < 600:
            # TODO: we don't log data from the /api/auth/registration/ endpoint, because there is a password in the data.
            #  We should just remove this password from body and show all the other data.
            message = f'Error response {response.status_code}'
            if request.path != '/api/auth/registration/':
                logger.warning(message,
                               extra={'message_id': 'error_logging_middleware',
                                      "request_query": request.GET,
                                      "request_body": request_body,
                                      "request_path": request.path,
                                      "response_content": response.content})
            else:
                logger.warning(message,
                               extra={'message_id': 'error_logging_middleware',
                                      "request_path": request.path,
                                      "response_content": response.content})
        return response
    return middleware
