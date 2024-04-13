#!/usr/bin/env python3
"""
Auth class
"""

from flask import request
from typing import List, TypeVar
import os


class Auth:
    """ Auth class for managing API authentication.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks if authentication is required
        """
        if ((path is None) or ((excluded_paths is None)
                               or (len(excluded_paths) == 0))):
            return True

        if path[-1] != '/':
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                prefix = excluded_path[:-1]
                if path.startswith(prefix):
                    return False
            elif path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Method to retrieve and validate
        the Authorization header from the request.

        Args:
            request: The Flask request object.

        Returns:
            str: The value of the Authorization
            header if present, otherwise None.
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method to get the current user based on the request.

        Args:
            request (flask.Request): The Flask request object.

        Returns:
            TypeVar('User'): The current user.
        """
        return None

    def session_cookie(self, request=None) -> str:
        """ Returns a cookie value from a request
        """
        if request is None:
            return None

        session_name = os.getenv("SESSION_NAME")
        if session_name is None:
            return None

        return request.cookies.get(session_name)
