
import grpc

from proto.v1.tracker import customers_pb2_grpc
from proto.v1.tracker import customers_pb2
from proto.v1.response import status_pb2

class CustomerService(customers_pb2_grpc.CustomerServiceServicer):

    def CreateCustomer(self, request, context):
        """
        Create a customer

        :param request: A CreateCustomerRequest
        :param context: The grpc context
        """
        print("Creating a customer: {}".format(request.customer))

        customer_name = request.customer.name + ' Yo'

        return customers_pb2.CreateCustomerResponse(
            customer=customers_pb2.Customer(
                id=42,
                name=customer_name,
            ),
            status=status_pb2.Status(code=200),
        )


def register(server):
    """Register service at server"""
    service = CustomerService()

    return customers_pb2_grpc \
        .add_CustomerServiceServicer_to_server(service, server)

