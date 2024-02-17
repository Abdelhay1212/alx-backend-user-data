#!/usr/bin/env python3
""" Basic auth """
import base64
from typing import Tuple
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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """decode base64 authorization header
        """
        if base64_authorization_header is None or \
                type(base64_authorization_header) != str:
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_str = decoded_bytes.decode('utf-8')
            return decoded_str
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """extract user credentials
        """
        if decoded_base64_authorization_header is None \
                or type(decoded_base64_authorization_header) != str \
                or ":" not in decoded_base64_authorization_header:
            return (None, None)
        credentials = decoded_base64_authorization_header.split(':')
        return (credentials[0], credentials[1])
