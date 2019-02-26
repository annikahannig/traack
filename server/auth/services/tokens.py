
"""
Auth tokens service
"""

import secrets
from datetime import datetime, timedelta

import jwt

from db.session import Session, session
from auth.models import User


TOKEN_SECRET_KEY = "make_configurable!"
TOKEN_LIFETIME_MINUTES = 30


def make_api_key():
    """Generate a random api key"""
    return secrets.token_hex(8)


def make_api_secret():
    """Generate a  random api secret"""
    return secrets.token_urlsafe(64)


def create_token_for_user(user):
    """Create a fresh user token"""
    now = datetime.utcnow()
    payload = {
        "sub": user.id,
        "iat": now,
        "exp": now + timedelta(minutes=TOKEN_LIFETIME_MINUTES),
    }

    return jwt.encode(payload, TOKEN_SECRET_KEY, algorithm="HS256")


def authenticate_auth_token(token):
    """Authenticate a jwt auth token"""
    try:
        payload = jwt.decode(token, TOKEN_SECRET_KEY)
    except:
        return None

    user_id = payload["sub"]

    s = Session()
    user = s.query(User).filter_by(id=user_id).first()
    s.close()

    return user


def authenticate_api_key(key, secret):
    """Authenticate an API key"""
    s = Session()
    user = s.query(User).filter_by(api_key=key, api_secret=secret).first()
    s.close()

    return user

