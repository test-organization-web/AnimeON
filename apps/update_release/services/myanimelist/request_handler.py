import requests
from .exceptions import APIException
from .json_serializer import JsonResponse


class APICaller(object):

    def __init__(self, base_url, headers):
        self._base_url = base_url
        self._headers = headers

    def call(self, uri, method="get", params=None, *args, **kwargs):
        requester = getattr(requests, method.lower())
        url = self._base_url + uri
        response = requester(url=url,
                             headers=self._headers,
                             params=params,
                             *args,
                             **kwargs)
        if response.status_code < 400:
            if method in ["get", "post", "patch", "put"]:
                try:
                    return response.json()
                except Exception as error:
                    raise APIException(
                        f"Error: {response.status_code}: {error}, {url}",
                        response)
            elif method == "delete":
                return response.status_code
        else:
            raise APIException(
                f"Error: {response.status_code}: {response.content}, {url}",
                response)
