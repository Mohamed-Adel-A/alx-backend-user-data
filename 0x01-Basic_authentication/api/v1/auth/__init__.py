#!/usr/bin/env python3
""" Module for authentication
"""
from typing import List

class Auth:
    """ Class for authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks if authentication is required
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """ Returns authorization header
        """
        if request is None or "Authorization" not in request.headers:
            return None
        return request.headers["Authorization"]

    def current_user(self, request=None) -> str:
        """ Returns current user
        """
        return None
