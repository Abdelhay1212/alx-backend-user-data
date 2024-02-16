#!/usr/bin/env python3
""" Basic auth """
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """basic auth
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """extract base64 authorization header
        """
        if authorization_header is None or type(authorization_header) != str \
                or not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]
