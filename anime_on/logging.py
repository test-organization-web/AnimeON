from django.http.request import HttpRequest
from contextlib import contextmanager
import logging
import json
import traceback
import threading


thread_context = threading.local()


def get_request_id():
    return getattr(thread_context, "request_id", None)


def set_request_id(request_id):
    thread_context.request_id = request_id


@contextmanager
def request_id_context(request_id):
    try:
        yield set_request_id(request_id)
    finally:
        # cleanup request_id explicitly
        # as gunicorn use threads again to handle new requests
        # even though we set a new one at the beginning of every request
        # btw with gunicorn+gevent requests can't see context from previous requests even without this
        set_request_id(None)


def default(obj):  # add more types to pass their objects to loggers
    if callable(obj):
        return obj()
    if isinstance(obj, HttpRequest):
        result = {"method": obj.method, "path": obj.path}
        if obj.GET:
            result["query"] = dict(obj.GET)
        return result
    return str(obj)  # any type will be converted to json, even if the result's ugly


class FormatterJSON(logging.Formatter):
    def format(self, record):
        exclude = (
            'msg', 'args', 'exc_text', 'stack_info',
            'relativeCreated', 'msecs',
            'thread', 'threadName', 'processName', 'process',
        )
        log_data = {k: v for k, v in record.__dict__.items() if k not in exclude}
        log_data["asctime"] = self.formatTime(record, self.datefmt)
        log_data["message"] = record.getMessage()
        log_data["logger"] = log_data.pop("name")
        log_data["request_id"] = get_request_id()
        exc_info = log_data.pop("exc_info")
        if exc_info:
            log_data["exception"] = traceback.format_exception(*exc_info)
        return json.dumps(log_data, default=default)
