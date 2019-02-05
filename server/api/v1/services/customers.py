
import grpc

from proto.v1.tracker import customers_pb2_grpc
from proto.v1.tracker import customers_pb2
from proto.v1.response import status_pb2
from customers.validators import validate_customer
from utils.grpc import log_requests, catch_errors
from utils.exceptions import exception_to_runtime_error
from db.session import Session
from customers.models import Customer


@log_requests
class CustomerService(customers_pb2_grpc.CustomerServiceServicer):

    @catch_errors(customers_pb2.CreateCustomerResponse)
    def CreateCustomer(self, request, context):
        """
        Create a customer

        :param request: A CreateCustomerRequest
        :param context: The grpc context
        """
        # Validate customer
        errors = validate_customer(request.customer)
        if errors:
            return customers_pb2.CreateCustomerResponse(
                status=status_pb2.Status(code=400, data_errors=errors),
            )

        # Add customer to database
        db = Session()
        customer = Customer(request.customer)
        try:
            db.add(customer)
            db.commit()

            return customers_pb2.CreateCustomerResponse(
                customer=customer.to_message(customers_pb2.Customer),
                status=status_pb2.Status(code=200),
            )

        except Exception as e:
            db.rollback()

            return customers_pb2.CreateCustomerResponse(
                status=status_pb2.Status(
                    code=500,
                    runtime_errors=[exception_to_runtime_error(e)]),
            )

        finally:
            db.close()

    @catch_errors(customers_pb2.ListCustomersResponse)
    def ListCustomers(self, request, context):
        """
        List all customers

        :param request: A ListCustomersRequest
        :param context: the grpc context
        """
        db = Session()
        customers = db.query(Customer).all()

        return customers_pb2.ListCustomersResponse(
            customers=[c.to_message() for c in customers],
            status=status_pb2.Status(code=200))


    @catch_errors(customers_pb2.DeleteCustomersResponse)
    def DeleteCustomer(self, request, context):
        """
        Delete a customer

        :param request: A ListCustomerRequest
        :param context: The Grpc context
        """
        return customers_pb2.DeleteCustomerResponse()




def register(server):
    """Register service at server"""
    service = CustomerService()

    return customers_pb2_grpc \
        .add_CustomerServiceServicer_to_server(service, server)

