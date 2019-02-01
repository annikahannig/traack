
"""
Validation Helpers
"""

from functools import wraps

from google.protobuf.json_format import MessageToDict
from google.protobuf.pyext.cpp_message import GeneratedProtocolMessageType

from proto.v1.response import errors_pb2


def errors_to_messages(errors):
    """Generate a list of validation errors"""
    return [errors_pb2.ValidationError(
                field=field,
                messages=error_messages,
           ) for field, error_messages in errors.items()]


def protobuf_validator(validator):
    @wraps(validator)
    def validate_message(message):
        # Check if we have a protobuf message type here.
        if type(type(message)) == GeneratedProtocolMessageType:
            message = MessageToDict(message)

        result, errors = validator(message)

        # Wrap errors in ValidationError messages
        return result, errors_to_messages(errors)

    return validate_message

