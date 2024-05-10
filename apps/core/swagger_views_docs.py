from enum import Enum


class SwaggerTags(str, Enum):
    # services
    AUTH = 'Auth'
    USER = 'User'
    ANIME = 'Anime'


class BaseSwaggerAPIViewDoc:
    tags = []
    summary = ...
    description = ...
    responses = None
