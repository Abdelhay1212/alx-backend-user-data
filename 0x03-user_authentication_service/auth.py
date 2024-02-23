#!/usr/bin/env python3
"""auth module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """hash a given password
    """
    salt = bcrypt.gensalt()
    bytes_passwd = bytes(password, 'utf-8')
    return bcrypt.hashpw(bytes_passwd, salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register a user by email and password
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User <{email}> already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(
                email=email, hashed_password=hashed_password)
            return new_user