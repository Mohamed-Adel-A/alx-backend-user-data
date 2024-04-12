#!/usr/bin/env python3
""" Module for auth
"""
from flask import request
from typing import List, TypeVar
from api.v1.auth import Auth

class Auth(Auth):
    """ Class for auth
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks if authentication is required
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != '/':
            path += '/'
        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """ Returns authorization header
        """
        if request is None or "Authorization" not in request.headers:
            return None
        return request.headers["Authorization"]

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns current user
        """
        return None
