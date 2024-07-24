import logging
import boto3

from datetime import datetime, UTC
from uuid import uuid4

from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from django.utils import timezone


logger = logging.getLogger(__name__)
scheduler_client = None
events_client = None


def get_scheduler_client():
    global scheduler_client
    if scheduler_client is None:
        scheduler_client = boto3.client('scheduler')
    return scheduler_client


def schedule_command(
    command: str,
    start_time: datetime = None,
    schedule_expression: str = None,
    args: list = None,
    kwargs: dict = None,
):
    """
    start_time: datetime, only for one-time scheduling case

    schedule_expression: str,
     at(2022-11-20T13:00:00) - one-time scheduling case
     rate(5 minutes)         - recurrent scheduling case
     cron(15 10 ? * 6L 2022) - recurrent scheduling case

    Example call: schedule_command(start_time=datetime.utcnow()+timedelta(seconds=30), command="migrate")
    """
    queue_arn = settings.SQS_QUEUE_ARN
    if not queue_arn:
        logger.warning("SQS_QUEUE_ARN is not configured. Scheduling task has been skipped.")
        return

    role_arn = settings.SCHEDULER_RUN_TASK_ROLE_ARN
    if not role_arn:
        logger.warning("SCHEDULER_RUN_TASK_ROLE_ARN is not configured. Scheduling task has been skipped.")
        return

    if start_time is not None and schedule_expression is not None:
        raise ValueError('Only one of start_time and schedule_expression required')

    if schedule_expression is None:
        if start_time is None:
            start_time = timezone.now()

        # start_time to UTC
        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=UTC)
        elif start_time.tzinfo != UTC:
            start_time = start_time.astimezone(UTC)

        schedule_expression = f"at({start_time.strftime('%Y-%m-%dT%H:%M:%S')})"

    command_input = {
        "command": command,
        "args": [],
        "kwargs": {},
    }
    if args:
        command_input["args"] = args
    if kwargs:
        command_input["kwargs"] = kwargs

    task_id = f'Task-{command[:26]}-{uuid4().hex}'  # max length of 'task_id' is 64 chars
    command_input = DjangoJSONEncoder().encode(command_input)

    get_scheduler_client().create_schedule(
        Name=task_id,
        ActionAfterCompletion="DELETE",
        FlexibleTimeWindow={'Mode': 'OFF'},
        ScheduleExpression=schedule_expression,
        ScheduleExpressionTimezone='UTC',
        Target={
            'Arn': queue_arn,
            'Input': command_input,
            'RoleArn': role_arn,
        },
    )
    logger.info('A task has been scheduled.',
                extra={'message_id': 'schedule_command_task_registered',
                       'command_name': command,
                       'command_input': command_input,
                       'schedule_expression': schedule_expression})
