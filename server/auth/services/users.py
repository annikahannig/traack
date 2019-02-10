
"""
Users Service
"""

import bcrypt

from db.session import Session
from auth import models


def hash_password(passwd):
    """Make password hash"""
    if not passwd:
        return None

    salt = bcrypt.gensalt(13)
    return bcrypt.hashpw(passwd.decode("utf-8"), salt)


def create_user(params: dict):
    """
    Create a user
    """
    password_hash = hash_password(params.get("password"))
    del params["password"]
    params["password_hash"] = password_hash

    user = models.User(**params)

    db = Session()
    db.add(user)
    db.commit()
    db.close()

    return user
