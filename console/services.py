
import importlib
from importlib import reload

import grpc

_PROTO_PREFIX = "proto"

_GRPC_HOST = None
_GRPC_CHANNEL = None


def init(host):
    """Initialize Client"""
    # Set configuration variabls
    global _GRPC_HOST
    _GRPC_HOST = host

    print("grpc service console          v.0.1.0")
    print("")
    print("Configuration:")
    print(" - Host:\t\t{}".format(_GRPC_HOST))
    print("")
    print("Usage:")
    print("  get_service('v1.project.services.Service')")
    print("    will return a configured ServiceStub object.")
    print("  get_messages('v1.project.services')")
    print("    will return the module containing the messages.")
    print("")

    connect()


def _parse_fqsn(fqsn):
    """
    Get an service module name and service class from
    fully qualified service name.
    """
    tokens = fqsn.split(".")

    service_class = tokens[-1] + "Stub"

    module_path = ".".join(tokens[:-1])
    module_name = _PROTO_PREFIX + "." + module_path + "_pb2_grpc"

    return module_name, service_class


def get_service(fqsn):
    """
    Get a service instance.

    Naming convention, starting from proto directory
    is v1.tracker.customers.CustomerService
    for an proto.v1.tracker.customers_pb2_grpc.CustomerServiceStub
    """
    module_name, service_name = _parse_fqsn(fqsn)
    try:
        service_module = importlib.import_module(module_name)
    except ImportError:
        print("Could not load service: Module `{}` not found.".format(
            module_name))
        return None

    try:
        service_class = getattr(service_module, service_name)
    except AttributeError:
        print("Could not load service: `{}` is not part of `{}`.".format(
            service_name, module_name))
        return None

    service = service_class(_GRPC_CHANNEL)

    return service


def get_messages(fqmn):
    """
    Get a messages module.

    Naming convention is as with the service:
        v1.tracker.customers
    will yield
        proto.v1.tracker.customers_pb2
    """
    module_name = "{}.{}_pb2".format(_PROTO_PREFIX, fqmn)

    try:
        module = importlib.import_module(module_name)
    except ImportError:
        print("Could not load messages: Module `{}` not found.".format(
            module_name))
        return None

    return module


def connect():
    """Create grpc channel"""
    global _GRPC_CHANNEL
    _GRPC_CHANNEL = grpc.insecure_channel(_GRPC_HOST)


