#!/usr/bin/env python3
""" Auth class """
from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        if path.endswith('/'):
            path_no_slash = path[:-1]
        path_no_slash = path

        for path in excluded_paths:
            if path.endswith('/'):
                if path_no_slash == path[:-1]:
                    return False
            if path_no_slash == path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """authorization header
        """
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """current user
        """
        return None
