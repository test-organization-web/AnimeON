from django import template
from django.conf import settings

from typing import Union

from apps.support.models import HelpAppeal, RightholderAppeal

register = template.Library()


@register.simple_tag
def ticket_is_can_be_assigned_to_user(ticket: Union[RightholderAppeal, HelpAppeal], user: settings.AUTH_USER_MODEL):
    return ticket.is_can_be_assigned_to_user(user)


@register.simple_tag
def ticket_is_can_be_resolved(ticket: Union[RightholderAppeal, HelpAppeal], user: settings.AUTH_USER_MODEL):
    return ticket.is_can_be_resolved(user)


@register.simple_tag
def ticket_is_can_be_unassigned_by_user(ticket: Union[RightholderAppeal, HelpAppeal], user: settings.AUTH_USER_MODEL):
    return ticket.is_can_be_unassigned_by_user(user)
