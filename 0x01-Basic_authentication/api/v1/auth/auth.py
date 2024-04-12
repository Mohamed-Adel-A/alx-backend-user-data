#!/usr/bin/env python3
"""
Auth class
"""

from flask import request
from typing import List, TypeVar


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
        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """ Method to get the Authorization header from the request.

        Args:
            request (flask.Request): The Flask request object.

        Returns:
            str: The Authorization header value.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method to get the current user based on the request.

        Args:
            request (flask.Request): The Flask request object.

        Returns:
            TypeVar('User'): The current user.
        """
        return None
