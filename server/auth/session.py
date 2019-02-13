
"""
Authenticated session
"""

from datetime import datetime
from db.session import Session as DbSession
from auth.models import User

class Session:
    """A api session"""
    def __init__(self, user, token_payload, token):
        """Initialize Session"""
        self.user = user
        self.token = token

        # Unpack token payload
        if token_payload:
            self.expires_at = token_payload["exp"]
            self.issued_at = token_payload["iat"]
            self.user_id = token_payload["sub"]

    @property
    def ttl(self):
        """Calculate session ttl"""
        if not self.expires_at:
            return 0

        return (self.expires_at - datetime.utcnow()).total_seconds()

    @property
    def user(self):
        """Load user on demand"""
        if not self.user_id:
            return None

        db = DbSession()
        user = db.Query(User).filter_by(self.user_id)
        db.close()

        return user
