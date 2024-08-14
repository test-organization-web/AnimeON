from django.db import models
from django.conf import settings
from django.utils.html import format_html
from django.urls import reverse

from apps.core.models import CreatedDateTimeMixin
from apps.support.choices import (
    RightholderAppealEvents, RightholderAppealStatus, HelpAppealEvents, HelpAppealStatus,
)


class RightholderAppeal(CreatedDateTimeMixin, models.Model):
    organization = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    email = models.EmailField()
    release_url = models.JSONField()
    document_url = models.JSONField()
    explanation = models.TextField()
    message = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    status = models.CharField(choices=RightholderAppealStatus.choices,  max_length=50, blank=True)
    assigned = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='rightholder_appeal'
    )

    def is_can_be_resolved(self, user):
        return self.assigned == user and self.status != HelpAppealStatus.RESOLVED

    def is_can_be_assigned_to_user(self, user):
        return self.assigned != user or self.status in (HelpAppealStatus.OPEN, HelpAppealStatus.CREATED)

    def is_can_be_unassigned_by_user(self, user):
        return self.assigned == user and self.status != HelpAppealStatus.RESOLVED

    def process_assigned(self, history_record: 'RightholderAppealHistory'):
        self.assigned = history_record.user
        self.save(update_fields=['assigned'])
        self.process_new_history_event(event=RightholderAppealEvents.IN_PROGRESS, user=history_record.user)

    def process_unassigned(self):
        self.assigned = None
        self.save(update_fields=['assigned'])
        self.process_new_history_event(event=RightholderAppealEvents.OPEN)

    def process_new_history_event(self, event: RightholderAppealEvents, **kwargs) -> 'RightholderAppealHistory':
        old_status = self.status

        history_record = self.rightholderappeal_history.create(event=event, **kwargs)
        self.revaluate_status()

        if self.status != old_status:
            history_record.status = self.status
            history_record.save(update_fields=['status'])

        if event == RightholderAppealEvents.ASSIGNED:
            self.process_assigned(history_record)

        if event == RightholderAppealEvents.UNASSIGNED:
            self.process_unassigned()

        return history_record

    def revaluate_status(self):
        """
        Note: should be called AFTER the voiceover history has been created
        """

        history = self.rightholderappeal_history

        if history.filter(event=RightholderAppealEvents.RESOLVED).exists():
            new_status = RightholderAppealEvents.RESOLVED
        else:
            last_obj = history.last()

            if last_obj.event == RightholderAppealEvents.IN_PROGRESS:
                new_status = RightholderAppealEvents.IN_PROGRESS
            else:
                new_status = RightholderAppealEvents.OPEN

        if self.status != new_status:
            self.status = new_status
            self.save(update_fields=["status"])


class RightholderAppealHistory(CreatedDateTimeMixin, models.Model):
    appeal = models.ForeignKey('RightholderAppeal', on_delete=models.CASCADE, related_name='rightholderappeal_history')
    event = models.CharField(choices=RightholderAppealEvents.choices, max_length=50)
    message = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(choices=RightholderAppealStatus.choices, blank=True, max_length=100)

    def get_additional_information_html_display(self) -> str:
        if self.event == HelpAppealEvents.ASSIGNED:
            user_change_url = reverse('admin:{}_{}_change'.format(
                self.user._meta.app_label, self.user._meta.model_name
            ), args=(self.user.id,))
            user_link = format_html('<a href="{}">{}</a>', user_change_url, self.user)
            return f'User: {user_link}'
        return ''


class HelpAppeal(CreatedDateTimeMixin, models.Model):
    title = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    status = models.CharField(choices=HelpAppealStatus.choices, max_length=50, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    assigned = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='help_appeal'
    )

    def is_can_be_resolved(self, user):
        return self.assigned == user and self.status != HelpAppealStatus.RESOLVED

    def is_can_be_assigned_to_user(self, user):
        return self.assigned != user or self.status in (HelpAppealStatus.OPEN, HelpAppealStatus.CREATED)

    def is_can_be_unassigned_by_user(self, user):
        return self.assigned == user and self.status != HelpAppealStatus.RESOLVED

    def process_assigned(self, history_record: 'HelpAppealHistory'):
        self.assigned = history_record.user
        self.save(update_fields=['assigned'])
        self.process_new_history_event(event=HelpAppealEvents.IN_PROGRESS, user=history_record.user)

    def process_unassigned(self):
        self.assigned = None
        self.save(update_fields=['assigned'])
        self.process_new_history_event(event=HelpAppealEvents.OPEN)

    def process_new_history_event(self, event: HelpAppealEvents, **kwargs) -> 'HelpAppealEvents':
        old_status = self.status

        history_record = self.helpappeal_history.create(event=event, **kwargs)
        self.revaluate_status()

        if self.status != old_status:
            history_record.status = self.status
            history_record.save(update_fields=['status'])

        if event == HelpAppealEvents.ASSIGNED:
            self.process_assigned(history_record)

        if event == HelpAppealEvents.UNASSIGNED:
            self.process_unassigned()

        return history_record

    def revaluate_status(self):
        """
        Note: should be called AFTER the voiceover history has been created
        """

        history = self.helpappeal_history

        if history.filter(event=RightholderAppealEvents.RESOLVED).exists():
            new_status = RightholderAppealEvents.RESOLVED
        else:
            last_obj = history.last()

            if last_obj.event == RightholderAppealEvents.IN_PROGRESS:
                new_status = RightholderAppealEvents.IN_PROGRESS
            elif last_obj.event == RightholderAppealEvents.OPEN:
                new_status = RightholderAppealEvents.OPEN
            else:
                new_status = RightholderAppealEvents.CREATED

        if self.status != new_status:
            self.status = new_status
            self.save(update_fields=["status"])


class HelpAppealHistory(CreatedDateTimeMixin, models.Model):
    appeal = models.ForeignKey('HelpAppeal', on_delete=models.CASCADE, related_name='helpappeal_history')
    event = models.CharField(choices=HelpAppealEvents.choices, max_length=50)
    message = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(choices=HelpAppealStatus.choices, blank=True, max_length=100)

    def get_additional_information_html_display(self) -> str:
        if self.event == HelpAppealEvents.ASSIGNED:
            user_change_url = reverse('admin:{}_{}_change'.format(
                self.user._meta.app_label, self.user._meta.model_name
            ), args=(self.user.id,))
            user_link = format_html('<a href="{}">{}</a>', user_change_url, self.user)
            return f'User: {user_link}'
        return ''
