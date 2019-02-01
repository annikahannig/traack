
"""
Models helper
"""

from functools import wraps

from sqlalchemy.ext.declarative.api import DeclarativeMeta
from google.protobuf.json_format import MessageToDict
from google.protobuf.pyext.cpp_message import GeneratedProtocolMessageType



class ProtobufModelMixinMeta(DeclarativeMeta):
    def __init__(cls, name, bases, dict_):

        # When we are making the minxin class, ignore DeclarativeMeta
        if name == "ProtobufModelMixin":
            return type.__init__(cls, name, bases, dict_)

        # Make model class
        model_class = super(ProtobufModelMixinMeta, cls).__init__(name, bases, dict_)

        # Patch init to provide initialization with a protobuf message
        model_init = getattr(cls, "__init__")

        def __model_init__(self, *args, **kwargs):
            if len(args) > 0:
                arg = args[0]

                # Check arg type: In case this is a message,
                # use the message as dict to initialize the model
                if type(type(arg)) == GeneratedProtocolMessageType:
                    initial = MessageToDict(arg)
                    return model_init(self, **initial)

            return model_init(self, *args, **kwargs)

        setattr(cls, "__init__", __model_init__)

        return model_class



class ProtobufModelMixin(metaclass=ProtobufModelMixinMeta):
    def to_dict(self):
        """Convert model to dict"""
        return {c.key: getattr(self, c.key)
                for c in self.__table__.columns}


    def to_message(self, pb_message_type):
        """"Convert to protobuf message type"""
        return pb_message_type(**self.to_dict())

