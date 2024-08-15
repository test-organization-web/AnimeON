from django.contrib import admin, messages
from django.urls import reverse
from django.utils.html import format_html
from django.urls import path
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from rest_framework import status

from django_admin_inline_paginator.admin import TabularInlinePaginated
from rangefilter.filters import DateRangeFilter
from adminfilters.combo import ChoicesFieldComboFilter

from apps.support.admin_action import assigned_tickets
from apps.core.admin import ReadOnlyPermissionsMixin
from apps.core.utils import get_instance_or_ajax_redirect
from apps.support.models import RightholderAppeal, HelpAppeal, RightholderAppealHistory, HelpAppealHistory
from apps.support.choices import HelpAppealEvents, RightholderAppealEvents


class RightholderAppealHistoryInline(ReadOnlyPermissionsMixin, TabularInlinePaginated):
    model = RightholderAppealHistory
    fields = ('created', 'who_created_the_entry', 'display_status', 'display_event')
    readonly_fields = ('created', 'who_created_the_entry', 'display_status', 'display_event')
    ordering = ('-created',)
    extra = 0
    verbose_name = 'History'
    verbose_name_plural = 'History'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

    @admin.display(description='By Who')
    def who_created_the_entry(self, obj: RightholderAppealHistory):
        if obj.user is not None:
            user_change_url = reverse('admin:{}_{}_change'.format(
                obj.user._meta.app_label, obj.user._meta.model_name
            ), args=(obj.user.id,))
            user_link = format_html('<a href="{}">{}</a>', user_change_url, obj.user)
            return format_html('User: {}', user_link)
        elif obj.id is not None:
            return 'System'
        else:
            return self.get_empty_value_display()

    @admin.display(description='Status')
    def display_status(self, obj: RightholderAppealHistory):
        return obj.status or ''

    @admin.display(description='Message')
    def display_event(self, obj: RightholderAppealHistory):
        display_result = f"{obj.message or obj.get_event_display()} {obj.get_additional_information_html_display()}"
        return format_html(display_result)


@admin.register(RightholderAppeal)
class RightholderAppealAdmin(ReadOnlyPermissionsMixin, admin.ModelAdmin):
    list_display = ['created', 'title', 'status', 'email', 'organization', 'contact_person']
    inlines = [RightholderAppealHistoryInline]

    actions = [assigned_tickets]

    list_filter = [
        ('created', DateRangeFilter),
        ('status', ChoicesFieldComboFilter),
    ]

    class Media:
        css = {
            'all': (
                "//code.jquery.com/ui/1.11.1/themes/smoothness/jquery-ui.css",
                'admin/css/utils/modal.css',
                'admin/css/buttons.css',
            )
        }
        js = (
            '//code.jquery.com/jquery-1.11.1.min.js',
            '//code.jquery.com/ui/1.11.1/jquery-ui.min.js',
            '//cdn.jsdelivr.net/npm/js-cookie@3.0.1/dist/js.cookie.min.js',
            "admin/js/utils/modal.js",
            "admin/js/utils/add_modal.js",
            'admin/js/utils/confirm_modal.js',
        )

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('<str:object_id>/add-note/',
                 self.admin_site.admin_view(self.add_note),
                 name='rightholderappeal_add_note'),
            path('<str:object_id>/assigned/',
                 self.admin_site.admin_view(self.assigned),
                 name='rightholderappeal_assigned'),
            path('<str:object_id>/resolve/',
                 self.admin_site.admin_view(self.resolve),
                 name='rightholderappeal_resolve'),
            path('<str:object_id>/unassigned/',
                 self.admin_site.admin_view(self.unassigned),
                 name='rightholderappeal_unassigned'),
        ]
        return my_urls + urls

    @method_decorator(require_POST)
    @get_instance_or_ajax_redirect(error_message="Ticket does not exist!",
                                   redirect_url='admin:support_rightholderappeal_changelist')
    def resolve(self, request, object_id, instance: HelpAppeal):
        if instance.is_can_be_resolved(user=request.user):
            instance.process_new_history_event(
                event=HelpAppealEvents.RESOLVED,
                user=request.user,
            )
            self.message_user(request, "The ticket has been successfully resolved!", level=messages.SUCCESS)
            return JsonResponse(data={
                'redirectUrl': reverse('admin:support_rightholderappeal_change', args=(instance.id,))
            })
        else:
            self.message_user(request,
                              f"Ticket can not been resolve to the {request.user}!",
                              level=messages.INFO)
            return JsonResponse(data={
                'redirectUrl': reverse('admin:support_helpappeal_change', args=(instance.id,))
            })

    @method_decorator(require_POST)
    @get_instance_or_ajax_redirect(error_message="Ticket does not exist!",
                                   redirect_url='admin:support_rightholderappeal_changelist')
    def add_note(self, request, object_id, instance: RightholderAppeal):
        if request.POST.get('userComment', '') == '':
            return JsonResponse(data={}, status=status.HTTP_400_BAD_REQUEST)

        instance.process_new_history_event(
            event=RightholderAppealEvents.COMMENT,
            user=request.user,
            message=request.POST['userComment'],
        )

        self.message_user(request, "The comment has been successfully added!", level=messages.SUCCESS)
        return JsonResponse(data={
            'redirectUrl': reverse('admin:support_rightholderappeal_change', args=(instance.id,))
        })

    @method_decorator(require_POST)
    @get_instance_or_ajax_redirect(error_message="Ticket does not exist!",
                                   redirect_url='admin:support_rightholderappeal_changelist')
    def assigned(self, request, object_id, instance: RightholderAppeal):
        if instance.is_can_be_assigned_to_user(user=request.user):
            instance.process_new_history_event(
                event=RightholderAppealEvents.ASSIGNED,
                user=request.user,
            )

            self.message_user(request,
                              f"Ticket has been successfully assigned to the {request.user}!",
                              level=messages.SUCCESS)
            return JsonResponse(data={
                'redirectUrl': reverse('admin:support_rightholderappeal_change', args=(instance.id,))
            })
        else:
            self.message_user(request,
                              f"Ticket can not been assigned to the {request.user}!",
                              level=messages.INFO)
            return JsonResponse(data={
                'redirectUrl': reverse('admin:support_helpappeal_change', args=(instance.id,))
            })

    @method_decorator(require_POST)
    @get_instance_or_ajax_redirect(error_message="Ticket does not exist!",
                                   redirect_url='admin:support_rightholderappeal_changelist')
    def unassigned(self, request, object_id, instance: RightholderAppeal):
        if instance.is_can_be_resolved(user=request.user):
            instance.process_new_history_event(
                event=RightholderAppealEvents.UNASSIGNED,
                user=request.user,
            )

            self.message_user(request,
                              f"Ticket has been successfully unassigned to the {request.user}!",
                              level=messages.SUCCESS)
            return JsonResponse(data={
                'redirectUrl': reverse('admin:support_rightholderappeal_change', args=(instance.id,))
            })
        else:
            self.message_user(request,
                              f"Ticket can not been unassigned to the {request.user}!",
                              level=messages.INFO)
            return JsonResponse(data={
                'redirectUrl': reverse('admin:support_helpappeal_change', args=(instance.id,))
            })


class HelpAppealHistoryInline(ReadOnlyPermissionsMixin, TabularInlinePaginated):
    model = HelpAppealHistory
    fields = ('created', 'who_created_the_entry', 'display_status', 'display_event')
    readonly_fields = ('created', 'who_created_the_entry', 'display_status', 'display_event')
    ordering = ('-created',)
    extra = 0
    verbose_name = 'History'
    verbose_name_plural = 'History'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

    @admin.display(description='By Who')
    def who_created_the_entry(self, obj: HelpAppealHistory):
        if obj.user is not None:
            user_change_url = reverse('admin:{}_{}_change'.format(
                obj.user._meta.app_label, obj.user._meta.model_name
            ), args=(obj.user.id,))
            user_link = format_html('<a href="{}">{}</a>', user_change_url, obj.user)
            return format_html('User: {}', user_link)
        elif obj.id is not None:
            return 'System'
        else:
            return self.get_empty_value_display()

    @admin.display(description='Status')
    def display_status(self, obj: HelpAppealHistory):
        return obj.status or ''

    @admin.display(description='Message')
    def display_event(self, obj: RightholderAppealHistory):
        display_result = f"{obj.message or obj.get_event_display()} {obj.get_additional_information_html_display()}"
        return format_html(display_result)


@admin.register(HelpAppeal)
class HelpAppealAdmin(ReadOnlyPermissionsMixin, admin.ModelAdmin):
    list_display = ['created', 'title', 'status', 'email']
    inlines = [HelpAppealHistoryInline]

    list_filter = [
        ('created', DateRangeFilter),
        ('status', ChoicesFieldComboFilter),
    ]

    actions = [assigned_tickets]

    class Media:
        css = {
            'all': (
                "//code.jquery.com/ui/1.11.1/themes/smoothness/jquery-ui.css",
                'admin/css/utils/modal.css',
                'admin/css/buttons.css',
            )
        }
        js = (
            '//code.jquery.com/jquery-1.11.1.min.js',
            '//code.jquery.com/ui/1.11.1/jquery-ui.min.js',
            '//cdn.jsdelivr.net/npm/js-cookie@3.0.1/dist/js.cookie.min.js',
            "admin/js/utils/modal.js",
            "admin/js/utils/add_modal.js",
            'admin/js/utils/confirm_modal.js',
        )

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('<str:object_id>/add-note/',
                 self.admin_site.admin_view(self.add_note),
                 name='helpappeal_add_note'),
            path('<str:object_id>/assigned/',
                 self.admin_site.admin_view(self.assigned),
                 name='helpappeal_assigned'),
            path('<str:object_id>/resolve/',
                 self.admin_site.admin_view(self.resolve),
                 name='helpappeal_resolve'),
            path('<str:object_id>/unassigned/',
                 self.admin_site.admin_view(self.unassigned),
                 name='helpappeal_unassigned'),
        ]
        return my_urls + urls

    @method_decorator(require_POST)
    @get_instance_or_ajax_redirect(error_message="Ticket does not exist!",
                                   redirect_url='admin:support_helpappeal_changelist')
    def resolve(self, request, object_id, instance: HelpAppeal):
        if instance.is_can_be_resolved(user=request.user):
            instance.process_new_history_event(
                event=HelpAppealEvents.RESOLVED,
                user=request.user,
            )
            self.message_user(request, "The ticket has been successfully resolved!", level=messages.SUCCESS)
            return JsonResponse(data={
                'redirectUrl': reverse('admin:support_helpappeal_change', args=(instance.id,))
            })
        else:
            self.message_user(request,
                              f"Ticket can not been resolve to the {request.user}!",
                              level=messages.INFO)
            return JsonResponse(data={
                'redirectUrl': reverse('admin:support_helpappeal_change', args=(instance.id,))
            })

    @method_decorator(require_POST)
    @get_instance_or_ajax_redirect(error_message="Ticket does not exist!",
                                   redirect_url='admin:support_helpappeal_changelist')
    def add_note(self, request, object_id, instance: HelpAppeal):
        if request.POST.get('userComment', '') == '':
            return JsonResponse(data={}, status=status.HTTP_400_BAD_REQUEST)

        instance.process_new_history_event(
            event=HelpAppealEvents.COMMENT,
            user=request.user,
            message=request.POST['userComment'],
        )

        self.message_user(request, "The comment has been successfully added!", level=messages.SUCCESS)
        return JsonResponse(data={
            'redirectUrl': reverse('admin:support_helpappeal_change', args=(instance.id,))
        })

    @method_decorator(require_POST)
    @get_instance_or_ajax_redirect(error_message="Ticket does not exist!",
                                   redirect_url='admin:support_helpappeal_changelist')
    def assigned(self, request, object_id, instance: HelpAppeal):
        if instance.is_can_be_assigned_to_user(user=request.user):
            instance.process_new_history_event(
                event=HelpAppealEvents.ASSIGNED,
                user=request.user,
            )

            self.message_user(request, f"Ticket has been successfully assigned to the {request.user}!",
                              level=messages.SUCCESS)
            return JsonResponse(data={
                'redirectUrl': reverse('admin:support_helpappeal_change', args=(instance.id,))
            })
        else:
            self.message_user(request,
                              f"Ticket can not been assigned to the {request.user}!",
                              level=messages.INFO)
            return JsonResponse(data={
                'redirectUrl': reverse('admin:support_helpappeal_change', args=(instance.id,))
            })

    @method_decorator(require_POST)
    @get_instance_or_ajax_redirect(error_message="Ticket does not exist!",
                                   redirect_url='admin:support_helpappeal_changelist')
    def unassigned(self, request, object_id, instance: HelpAppeal):
        if instance.is_can_be_unassigned_by_user(user=request.user):
            instance.process_new_history_event(
                event=HelpAppealEvents.UNASSIGNED,
                user=request.user,
            )
            self.message_user(request, f"Ticket has been successfully unassigned to the {request.user}!",
                              level=messages.SUCCESS)
            return JsonResponse(data={
                'redirectUrl': reverse('admin:support_helpappeal_change', args=(instance.id,))
            })
        else:
            self.message_user(request,
                              f"Ticket can not been unassigned to the {request.user}!",
                              level=messages.INFO)
            return JsonResponse(data={
                'redirectUrl': reverse('admin:support_helpappeal_change', args=(instance.id,))
            })
