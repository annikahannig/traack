"""
Exception helpers
"""

from proto.v1.response import errors_pb2

def exception_to_runtime_error(exc):
    """Convert an exception into a protobuf runtime error"""
    name = type(exc).__name__
    message = str(exc)

    return errors_pb2.RuntimeError(exception=name,
                                   messages=[message])

