#!/usr/bin/env python3
'''
Session Authentication
'''
from .auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    ''' SessionAuth '''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        ''' creates a session ID for a user_id '''
        if user_id and isinstance(user_id, str):
            self.session_id = str(uuid.uuid4())
            self.user_id_by_session_id[self.session_id] = user_id
            return self.session_id
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        ''' returns a user ID based on a session ID '''
        if session_id and isinstance(session_id, str):
            return self.user_id_by_session_id.get(session_id)
        return None

    def current_user(self, request=None):
        ''' returns a user instance based on a cookie value '''
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        ''' deletes the user session/logout '''
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        try:
            del self.user_id_by_session_id[session_id]
        except Exception:
            pass
        return True
