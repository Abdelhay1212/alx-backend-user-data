#!/usr/bin/env python3
""" Basic auth """
import base64
from typing import Tuple, TypeVar
from api.v1.auth.auth import Auth
from models.user import User


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

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """user object from credentials
        """
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({'email': user_email})
            if not users:
                return None

            user = users[0]
            if not user.is_valid_password(user_pwd):
                return None
            return user
        except Exception:
            return None
