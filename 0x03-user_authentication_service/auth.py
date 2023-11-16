#!/usr/bin/env python3
'''
Authentication
'''
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
import uuid
from typing import Union


def _hash_password(password: str) -> bytes:
    ''' returns a hashed password '''
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_pwd


def _generate_uuid() -> str:
    ''' generate uuid '''
    return str(uuid.uuid4())


class Auth:
    '''Auth class to interact with the authentication database.
    '''

    def __init__(self):
        ''' initializes Auth instance '''
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        ''' saves user to database '''
        if not email or not password:
            return None
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        else:
            raise ValueError('User {} already exists'.format(email))

    def valid_login(self, email: str, password: str) -> bool:
        ''' validates user credentials '''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        ''' create user session '''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        else:
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        ''' find user by session id '''
        if session_id:
            try:
                user = self._db.find_user_by(session_id=session_id)
                return user
            except NoResultFound:
                return None
        return None

    def destroy_session(self, user_id: int) -> None:
        ''' destroys a session '''
        if user_id:
            self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        ''' generate reset password token '''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        else:
            pwd_token = str(uuid.uuid4())
            self._db.update_user(user.id, reset_token=pwd_token)
            return pwd_token

    def update_password(self, reset_token: str, password: str):
        ''' update password '''
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        else:
            user.hashed_password = _hash_password(password)
            user.reset_token = None
            return None
