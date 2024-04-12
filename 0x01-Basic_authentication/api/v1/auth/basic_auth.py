#!/usr/bin/env python3
""" Module for basic auth
"""
from api.v1.auth import Auth
from typing import List, TypeVar
from base64 import b64decode
from models.user import User

class BasicAuth(Auth):
    """ Class for basic auth
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Extracts the base64 part of the authorization header
        """
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        parts = authorization_header.split(' ')
        if parts[0] != 'Basic' or len(parts) != 2:
            return None
        return parts[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """ Decodes the base64 part of the authorization header
        """
        if base64_authorization_header is None or \
           not isinstance(base64_authorization_header, str):
            return None
        try:
            return b64decode(base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                  decoded_base64_authorization_header: str
                                  ) -> (str, str):
        """ Extracts the user email and password from the base64
        authorization header
        """
        if decoded_base64_authorization_header is None or \
           not isinstance(decoded_base64_authorization_header, str) or \
           ':' not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self,
                                     user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """ Returns the User instance based on his email and password
        """
        if user_email is None or user_pwd is None:
            return None
        users = User.search({'email': user_email})
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns current user
        """
        authorization_header = self.authorization_header(request)
        if authorization_header is None:
            return None
        base64_auth_header = self.extract_base64_authorization_header(
            authorization_header)
        if base64_auth_header is None:
            return None
        decoded_auth_header = self.decode_base64_authorization_header(
            base64_auth_header)
        if decoded_auth_header is None:
            return None
        user_email, user_pwd = self.extract_user_credentials(decoded_auth_header)
        if user_email is None or user_pwd is None:
            return None
        return self.user_object_from_credentials(user_email, user_pwd)
