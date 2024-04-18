from anime_on.logging import request_id_context
from django.shortcuts import redirect
from uuid import uuid4


def request_id_middleware(get_response):
    def middleware(request):
        request_id = request.headers.get("X-Request-ID") or uuid4().hex
        with request_id_context(request_id):
            response = get_response(request)
        response.headers['X-Request-ID'] = request_id
        return response
    return middleware


# raise Redirect(url) is useful, because you can call it from any place in your code
class Redirect(Exception):
    def __init__(self, url):
        self.url = url


class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, Redirect):
            return redirect(exception.url)
