
import grpc

from proto.v1.tracker import customers_pb2_grpc
from proto.v1.tracker import customers_pb2
from proto.v1.response import status_pb2
from customers.validators import validate_customer
from utils.grpc import log_requests


@log_requests
class CustomerService(customers_pb2_grpc.CustomerServiceServicer):

    def CreateCustomer(self, request, context):
        """
        Create a customer

        :param request: A CreateCustomerRequest
        :param context: The grpc context
        """

        customer = request.customer
        # print("Creating a customer: {}".format(customer))
        errors = validate_customer(customer)
        if errors:
            return customers_pb2.CreateCustomerResponse(
                status=status_pb2.Status(code=400, data_errors=errors),
            )


        return customers_pb2.CreateCustomerResponse(
            customer=customers_pb2.Customer(
                id=42,
                name=customer.name,
            ),
            status=status_pb2.Status(code=200),
        )


def register(server):
    """Register service at server"""
    service = CustomerService()

    return customers_pb2_grpc \
        .add_CustomerServiceServicer_to_server(service, server)

