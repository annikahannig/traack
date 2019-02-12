
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
    AuthenticateApiKeyRequest,
    AuthenticateApiKeyResponse,
)
from proto.v1.auth.users_pb2_grpc import UserServiceServicer


class TokenService(TokenServiceServicer):
    """
    Implement Token Service
    """
    def AuthenticateApiKey(self, request, context):
        """
        Authenticate an api key and create a
        session / auth token
        """
        print("Authenticating")
        print(request)


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
        .add_UserServiceSerivcer_to_server(user_service, server)
