
import sqlalchemy as sa

from db import models
from auth.services import secrets as secrets_svc
from utils.models import ProtobufModelMixin


class User(ProtobufModelMixin, models.Base):
    """
    The user in our service
    """
    __tablename__ = "auth_user"

    # Fields
    id = sa.Column(sa.Integer,
                   sa.Sequence("auth_user_id_seq"),
                   primary_key=True)

    username = sa.Column(sa.String(80),
                         unique=True,
                         nullable=False)

    password_hash = sa.Column(sa.String(80))

    # Serice access
    api_key = sa.Column(sa.String(16),
                        default=secrets_svc.make_api_key)
    api_secret = sa.Column(sa.String(86),
                        default=secrets_svc.make_api_secret)

    # Personal info
    first_name = sa.Column(sa.String(30), nullable=True)
    last_name = sa.Column(sa.String(30), nullable=True)
    email = sa.Column(sa.String(60), nullable=True)

    # Flags
    is_admin = sa.Column(sa.Boolean(), nullable=False)


class Token(ProtobufModelMixin, models.Base):
    """
    A token is more or less equivalent to a 'session'
    """
    __tablename__ = "auth_token"

    id = sa.Column(sa.Integer,
                   sa.Sequence("auth_token_id_seq"),
                   primary_key=True)

    bearer = sa.Column(sa.String(86),
                       nullable=True,
                       unique=True,
                       default=secrets_svc.make_api_secret)

    user_id = sa.Column(sa.Integer,
                        sa.ForeignKey("auth_user.id",
                                      ondelete="CASCADE"),
                        nullable=False)

    issued_at = sa.Column(sa.DateTime(timezone=True),
                          nullable=False)

    expires_at = sa.Column(sa.DateTime(timezone=True),
                           nullable=False)

