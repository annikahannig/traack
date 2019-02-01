
"""
GRPC helpers
"""

import logging
from functools import wraps

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
