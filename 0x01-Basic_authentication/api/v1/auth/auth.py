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

        new_excluded = list()
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                prefix = excluded_path[:-1]
                new_excluded.append(prefix)
            else:
                new_excluded.append(excluded_path)

        if path[-1] != '/':
            path += '/'
        if path not in new_excluded:
            return True
        return False

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
