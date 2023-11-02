#!/usr/bin/env python3
'''
Encrypting data
'''
import bcrypt
from bcrypt import hashpw


def hash_password(password: str) -> bytes:
    ''' encrypts password and returns the password in bytes '''
    pwd = password.encode()
    hashed_pwd = hashpw(pwd, bcrypt.gensalt())
    return hashed_pwd


def is_valid(hashed_password: bytes, password: str) -> bool:
    ''' check valid password '''
    return bcrypt.checkpw(password.encode(), hashed_password)
