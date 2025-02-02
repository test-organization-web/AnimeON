import logging

from dal import autocomplete

from rest_framework.views import exception_handler
from rest_framework.response import Response
from django_countries.data import COUNTRIES

from apps.core.utils import get_response_body_errors


logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    if response is not None:
        kwargs = {}
        data = exc.detail if hasattr(exc, 'detail') else str(exc)
        try:
            if isinstance(data, dict):
                kwargs.update({'errors': [error['message'] for error in data['messages']]})
            elif isinstance(data, list):
                kwargs.update({'errors': [error['message'] for error in data]})
            else:
                kwargs.update({'errors': data})
            response_data = get_response_body_errors(**kwargs)
            return Response(response_data, status=response.status_code, headers=response.headers)
        except Exception as error:
            logger.exception(error)
    return response


class CountryAutocomplete(autocomplete.Select2ListView):
    def get_list(self):
        return [[code, name] for code, name in COUNTRIES.items()]
