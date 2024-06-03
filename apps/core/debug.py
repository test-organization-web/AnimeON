import json
import logging
from functools import wraps

from django.views.debug import ExceptionReporter, SafeExceptionReporterFilter
from rest_framework.request import Request

logger = logging.getLogger(__name__)


def sensitive_drf_post_parameters(*parameters):
    """
    The method is the same as 'sensitive_post_parameters', but with supporting APIView from Django REST Framework
    Look at 'django.views.decorators.debug.sensitive_post_parameters' to get more information
    """

    def decorator(view):
        @wraps(view)
        def sensitive_drf_post_parameters_wrapper(request, *args, **kwargs):
            if isinstance(request, Request):  # The Request class from Django REST Framework
                request._request.sensitive_post_parameters = parameters or '__ALL__'
            else:  # just simple Django Request
                request.sensitive_post_parameters = parameters or '__ALL__'

            return view(request, *args, **kwargs)

        return sensitive_drf_post_parameters_wrapper

    return decorator


class JSONSafeExceptionReporterFilter(SafeExceptionReporterFilter):
    def get_json_data_parameters(self, request):
        """
        (https://docs.djangoproject.com/en/4.2/ref/request-response/#django.http.HttpRequest.POST)
        """
        if request is None or request.content_type != 'application/json':
            return {}

        try:
            if hasattr(request, 'json_body'):
                data = request.json_body.copy()
            else:
                try:
                    data = json.loads(request.body) if request.body else {}
                except json.decoder.JSONDecodeError:
                    return {"invalid_json_str": request.body}
        except Exception as e:
            logger.error('Unexpected error occurs in "get_json_data_parameters" of the exception reporter.',
                         extra={'message_id': 'get_json_data_parameters_unexpected_error',
                                'error_type': str(type(e)),
                                'error': str(e)})
            return {}

        sensitive_post_parameters = getattr(request, "sensitive_post_parameters", [])

        if self.is_active(request):
            if sensitive_post_parameters == "__ALL__":
                # Cleanse all parameters.
                for k in data:
                    data[k] = self.cleansed_substitute
            else:
                # Cleanse only the specified parameters.
                for param in sensitive_post_parameters:
                    if param in data:
                        data[param] = self.cleansed_substitute

        return data


class JSONExceptionReporter(ExceptionReporter):
    def __init__(self, *args, extra_log_data=None, **kwargs):
        self.extra_log_data = extra_log_data
        super().__init__(*args, **kwargs)

    def get_traceback_data(self):
        assert isinstance(self.filter, JSONSafeExceptionReporterFilter)

        context = super().get_traceback_data()
        context['extra_log_data'] = self.extra_log_data
        context['filtered_json_data_items'] = self.filter.get_json_data_parameters(self.request).items()
        return context
