
"""
Secrets Service
"""

import secrets

def make_api_key():
    """Generate a random api key"""
    return secrets.token_hex(8)


def make_api_secret():
    """Generate a  random api secret"""
    return secrets.token_urlsafe(64)
