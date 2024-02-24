#!/usr/bin/env python3
"""auth module
"""
import uuid
import bcrypt
from db import DB
from user import User
from typing import Union
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """hash a given password
    """
    salt = bcrypt.gensalt()
    bytes_passwd = bytes(str(password), 'utf-8')
    return bcrypt.hashpw(bytes_passwd, salt)


def _generate_uuid() -> str:
    """generate uuid
    """
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """valid login
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(bytes(password, 'utf-8'),
                              user.hashed_password):
                return True
            return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """create session
        """
        try:
            user = self._db.find_user_by(email=email)
            user.session_id = _generate_uuid()
            return user.session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """get user from session id
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """destroy session
        """
        self._db.update_user(user_id, session_id=None)
