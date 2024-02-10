#!/usr/bin/env python3
''' Encrypting passwords '''
import bcrypt


def hash_password(password: str) -> str:
    ''' passwords should NEVER be stored in plain text in a database '''

    salt = bcrypt.gensalt()
    password = password.encode('utf-8')
    hashed_passwd = bcrypt.hashpw(password, salt)
    return hashed_passwd
