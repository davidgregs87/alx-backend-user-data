#!/usr/bin/env python3
'''
Authentication Module
'''
from flask import request
from typing import List, TypeVar
import os


class Auth:
    ''' Auth class '''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        ''' require authentication '''
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        if path in excluded_paths:
            return False

        for excluded_path in excluded_paths:
            if excluded_path.startswith(path):
                return False
            elif path.startswith(excluded_path):
                return False
            elif excluded_path[-1] == '*':
                if path.startswith(excluded_path[:-1]):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        ''' authorization header '''
        if request is None:
            return None
        header = request.headers.get('Authorization')
        if header is None:
            return None
        return header

    def current_user(self, request=None) -> TypeVar('User'):
        ''' get current user '''
        return None

    def session_cookie(self, request=None):
        ''' returns a cookie value from a request '''
        if request is None:
            return None
        return request.cookies.get(os.getenv('SESSION_NAME'))
