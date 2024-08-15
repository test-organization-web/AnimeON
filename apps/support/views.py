from django.conf import settings
from django.core.mail import send_mail

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny

from apps.core.utils import swagger_auto_schema_wrapper, validate_request_data
from apps.support.models import RightholderAppeal, HelpAppeal
from apps.support.choices import RightholderAppealEvents, HelpAppealEvents
from apps.support.serializers import RightholderAppealSerializer, HelpAppealSerializer
from apps.support.swager_views_docs import RightholderAppealAPIViewDoc, HelpAppealAPIViewDoc
from apps.core.mixins import CheckIPSpam


class RightholderAppealAPIView(CheckIPSpam, APIView):
    spam_key = 'rightholder'
    permission_classes = (AllowAny,)
    request_serializer = RightholderAppealSerializer

    @swagger_auto_schema_wrapper(doc=RightholderAppealAPIViewDoc,
                                 request_serializer_cls=request_serializer,
                                 operation_id='create_rightholder_appeal')
    @validate_request_data(serializer_cls=request_serializer)
    def post(self, request, serializer: RightholderAppealSerializer):
        ticket: RightholderAppeal = serializer.save()
        if not request.user.is_anonymous:
            ticket.user = request.user
            ticket.save(update_fields=['user'])

        if settings.EMAIL_HOST:
            send_mail(subject=ticket.title, message=ticket.message, from_email=None,
                      recipient_list=[ticket.email, settings.EMAIL_HOST_USER], fail_silently=False, html_message=ticket.message)
        ticket.process_new_history_event(
            event=RightholderAppealEvents.OPEN
        )
        return Response(data={}, status=status.HTTP_201_CREATED)


class HelpAppealAPIView(CheckIPSpam, APIView):
    spam_key = 'help'
    permission_classes = (AllowAny,)
    request_serializer = HelpAppealSerializer

    @swagger_auto_schema_wrapper(doc=HelpAppealAPIViewDoc,
                                 request_serializer_cls=request_serializer,
                                 operation_id='create_help_appeal')
    @validate_request_data(serializer_cls=request_serializer)
    def post(self, request, serializer: HelpAppealSerializer):
        ticket: HelpAppeal = serializer.save()
        if not request.user.is_anonymous:
            ticket.user = request.user
            ticket.save(update_fields=['user'])

        if settings.EMAIL_HOST:
            send_mail(subject=ticket.title, message=ticket.message, from_email=None,
                      recipient_list=[ticket.email, settings.EMAIL_HOST_USER], fail_silently=False, html_message=ticket.message)
        ticket.process_new_history_event(
            event=HelpAppealEvents.OPEN
        )
        return Response(data={}, status=status.HTTP_201_CREATED)
