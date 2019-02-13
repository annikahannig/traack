
"""
Authentication related services
"""

from proto.v1.auth import (
    tokens_pb2,
    tokens_pb2_grpc,
    users_pb2,
    users_pb2_grpc,
)
from proto.v1.auth.tokens_pb2_grpc import (
    TokenServiceServicer,
)
from proto.v1.auth.tokens_pb2 import (
    AuthenticateApiKeyRequest,
    AuthenticateApiKeyResponse,
)
from proto.v1.auth.users_pb2_grpc import (
    UserServiceServicer,
)
from utils.grpc import log_requests, catch_errors
from auth.services import tokens as tokens_svc


@log_requests
class TokenService(TokenServiceServicer):
    """
    Implement Token Service
    """

    @catch_errors
    def AuthenticateApiKey(self, request, context):
        """
        Authenticate an api key and create a
        session / auth token
        """
        token = tokens_svc.authenticate_api_key(
            request.key, request.secret)


class UserService(UserServiceServicer):
    """
    User Service RPC Handler Implementation
    """

def register(server):
    """Register service at server"""
    token_service = TokenService()
    user_service = UserService()

    tokens_pb2_grpc \
        .add_TokenServiceServicer_to_server(token_service, server)

    users_pb2_grpc \
        .add_UserServiceServicer_to_server(user_service, server)

