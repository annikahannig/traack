
"""
GRPC helpers
"""

import logging
from functools import wraps

from proto.v1.response import status_pb2, errors_pb2

from utils.exceptions import exception_to_runtime_error

def _log_request(logger, method):
    @wraps(method)
    def log(self, request, context):
        peer = context.peer()

        # It is extremly weird that the logger prints this module's name
        # even though id(logger) == id(my.service.logger).
        # This looks like a bug and is a bit of a bummer.
        logger.info("{} :: {}".format(peer, method.__name__))

        return method(self, request, context)

    return log


def log_requests(cls):
    """
    Class decorator for wrapping all requests with a logging function
    """
    # Get logger for class module
    logger = logging.getLogger(cls.__module__)
    for attr in cls.__dict__:
        method = getattr(cls, attr)
        if callable(method):
            setattr(cls, attr, _log_request(logger, method))

    return cls


class catch_errors:
    """
    Catch exceptions and make error response
    """
    def __init__(self, response_cls):
        """Initialize decorator"""
        self.response_cls = response_cls

    def __call__(self, handler_fn):
        """Wrap function"""
        @wraps(handler_fn)
        def wrapper(*args, **kwargs):
            try:
                return handler_fn(*args, **kwargs)
            except Exception as e:
                status = status_pb2.Status(
                    code=500,
                    message="generic_error",
                    runtime_errors=[
                        exception_to_runtime_error(e),
                    ]
                )
                response = self.response_cls(status=status)
                return response

        return wrapper
