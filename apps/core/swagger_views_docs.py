from enum import Enum


class SwaggerTags(str, Enum):
    # services
    AUTH = 'Auth'
    USER = 'User'


class BaseSwaggerAPIViewDoc:
    tags = []
    summary = ...
    description = ...
    responses = None
