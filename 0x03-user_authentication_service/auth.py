#!/usr/bin/env python3
"""auth module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """hash a given password
    """
    salt = bcrypt.gensalt()
    bytes_passwd = bytes(password, 'utf-8')
    return bcrypt.hashpw(bytes_passwd, salt)
