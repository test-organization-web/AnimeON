import logging
from functools import wraps

from django.contrib import admin, messages
from django.template.response import TemplateResponse
from django.utils.translation import ngettext

from apps.support.choices import GeneralEvents

logger = logging.getLogger(__name__)


def require_confirmation(confirmation_action_name, user_comment_label_text=None, user_comment_is_required=False,
                         object_label=None):
    def decorator(func):
        @wraps(func)
        def wrapper(modeladmin, request, queryset):
            if request.POST.get("confirmation") is None:
                request.current_app = modeladmin.admin_site.name
                context = {
                    "action": request.POST.get("action"),
                    "queryset": queryset,
                    "confirmation_action_name": confirmation_action_name,
                    "user_comment_label_text": user_comment_label_text,
                    "user_comment_is_required": user_comment_is_required,
                    "object_label": object_label
                }
                return TemplateResponse(request, "admin/core/action/action_confirmation.html", context)

            return func(modeladmin, request, queryset)

        return wrapper

    return decorator


@admin.action(description='Пизначити тікет на себе')
@require_confirmation(confirmation_action_name='Пизначити тікет на себе', object_label='Тікет')
def assigned_tickets(modeladmin, request, queryset):
    all_count = queryset.count()
    user = request.user

    count_ticket = 0

    for ticket in queryset:
        if ticket.is_can_be_assigned_to_user(user=user):
            ticket.process_new_history_event(
                event=GeneralEvents.ASSIGNED,
                user=user
            )
            count_ticket += 1

    message = ngettext(
        '%(count_ticket)d тікет з %(all_count)d було призначено %(user)s.',
        '%(count_ticket)d тікетів з %(all_count)d було призначено %(user)s.',
        count_ticket,
    ) % {'all_count': all_count, 'count_ticket': count_ticket, 'user': user}

    modeladmin.message_user(request, message, level=messages.INFO)
