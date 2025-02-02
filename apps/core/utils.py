import os

from typing import Optional, Union, List, Dict
from functools import wraps

from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse


def get_response_body_errors(
        errors: Optional[Union[str, List[str]]] = None,
        serializer_errors: Optional[Union[Dict[str, List[str]], Dict[str, Dict[str, List[str]]]]] = None,
        base_location: str = None
) -> Dict[str, List[Dict[str, str]]]:
    """
    :return: dict. For example,
        {
            "errors": [
                {"message": "Required thing", "location": "dishes[0].beetroot"},
                {"message": "Retry after 30 seconds"}
            ]
        }
    """
    if errors is None and serializer_errors is None:
        raise ValueError('Must be provided either "errors" or "serializer_errors"')

    result_errors = []

    if serializer_errors is not None:
        for field_name, value in serializer_errors.items():
            location = f'{base_location}.{field_name}' if base_location else field_name
            if isinstance(value, dict):
                response_body_errors = get_response_body_errors(serializer_errors=value, base_location=location)
                result_errors.extend(response_body_errors['errors'])
            else:
                result_errors.extend([{'message': message, 'location': location} for message in value])

    if errors is not None:
        if isinstance(errors, str):
            errors = [errors]

        result_errors.extend([{'message': message} for message in errors])

    return {'errors': result_errors}


def swagger_auto_schema_wrapper(
        doc: 'BaseSwaggerAPIViewDoc',  # noqa: F821
        request_serializer_cls: Optional['Serializer'] = None,  # noqa: F821
        **kwargs,
):
    def wrapper(func):
        return swagger_auto_schema(
            tags=doc.tags,
            operation_summary=doc.summary,
            operation_description=doc.description,
            request_body=request_serializer_cls,
            responses=doc.responses,
            **kwargs
        )(func)

    return wrapper


def validate_request_data(serializer_cls, method: str = 'POST'):
    def wrapper(func):
        def inner(self, request, *args, **kwargs):
            ser = serializer_cls(data=request.data if method == 'POST' else request.query_params)
            if not ser.is_valid():
                errors = get_response_body_errors(serializer_errors=ser.errors)
                return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

            return func(self, request, *args, serializer=ser, **kwargs)

        return inner

    return wrapper


def get_extension(filename):
    if filename is None:
        return None
    return os.path.splitext(filename)[1].lstrip('.').lower()


def get_instance_or_ajax_redirect(error_message, redirect_url):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, object_id, *args, **kwargs):
            try:
                instance = self.model.objects.get(id=object_id)
            except self.model.DoesNotExist:
                self.message_user(request, error_message, level=messages.ERROR)
                return JsonResponse(data={'redirectUrl': reverse(redirect_url)})

            return view_func(self, request, object_id, *args, instance=instance, **kwargs)

        return _wrapped_view

    return decorator


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
