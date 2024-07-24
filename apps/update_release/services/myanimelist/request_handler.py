import requests
import logging

from requests import request
from typing import Optional
from .exceptions import APIException


logger = logging.getLogger(__name__)


class APICaller(object):

    def __init__(self, base_url: str, headers: dict):
        self._base_url = base_url
        self._headers = headers

    def call(self, uri: str, method: str = "get", params: Optional[dict] = None, *args, **kwargs) -> dict:
        requester: request = getattr(requests, method.lower())
        url = self._base_url + uri
        logger.info('Get request with params', extra={
            'message_id': 'myanimelist_request_handler_call',
            'method': method,
            'params': params,
            'url': url
        })
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
                        status_code=response.status_code,
                        message=f"Error: {response.status_code}: {error}, {url}",
                        response=response)
            elif method == "delete":
                return response.status_code
        else:
            raise APIException(
                status_code=response.status_code,
                message=f"Error: {response.status_code}: {response.content}, {url}",
                response=response)
