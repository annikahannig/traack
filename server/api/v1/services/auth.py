
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
from proto.v1.auth.users_pb2 import (
    WhoamiResponse,
    User,
)
from proto.v1.response.errors_pb2 import (
    AuthorizationError,
)
from proto.v1.response.status_pb2 import (
    Status
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

    @catch_errors(tokens_pb2.AuthenticateApiKeyResponse)
    def AuthenticateApiKey(self, request, context):
        """
        Authenticate an api key and create a
        session / auth token
        """
        user = tokens_svc.authenticate_api_key(
            request.key, request.secret)

        if not user:
            return AuthenticateApiKeyResponse(
                status=Status(
                    authorization_errors=[
                        AuthorizationError(
                            code="invalid_key_or_secret")],
                    code=403))

        # We have a valid user, issue a token
        token = tokens_svc.create_token_for_user(user)

        return AuthenticateApiKeyResponse(
            status=Status(code=200),
            auth_token=token,
        )


@log_requests
class UserService(UserServiceServicer):
    """
    User Service RPC Handler Implementation
    """

    @catch_errors(WhoamiResponse)
    def Whoami(self, request, context):
        """Reply with authorized user"""
        user = tokens_svc.authenticate_auth_token(request.authorization)
        if not user:
            return WhoamiResponse(
                status=Status(
                    code=403,
                    authorization_errors=[
                        AuthorizationError(code="invalid_token")
                    ]))

        # Respond with the current user
        return WhoamiResponse(
            status=Status(code=200),
            user=User(
                id=user.id,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
                is_admin=user.is_admin,
                api_key=user.api_key,
                api_secret=user.api_secret))


    @catch_errors(WhoamiResponse)
    def Whoami(self, request, context) -> WhoamiResponse:
        """Reply with authorized user"""
        user = tokens_svc.authenticate_auth_token(request.authorization)
        if not user:
            return WhoamiResponse(
                status=Status(
                    code=403,
                    authorization_errors=[
                        AuthorizationError(code="invalid_token")
                    ]))

        # Respond with the current user
        return WhoamiResponse(
            status=Status(code=200),
            user=User(
                id=user.id,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
                is_admin=user.is_admin,
                api_key=user.api_key,
                api_secret=user.api_secret))

def register(server):
    """Register service at server"""
    token_service = TokenService()
    user_service = UserService()

    tokens_pb2_grpc \
        .add_TokenServiceServicer_to_server(token_service, server)

    users_pb2_grpc \
        .add_UserServiceServicer_to_server(user_service, server)

