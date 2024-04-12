#!/usr/bin/env python3
"""
api/v1/auth/basic_auth.py
"""


from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """ BasicAuth class for managing basic authentication.
    """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Extracts the Base64 part of the Authorization
        header for Basic Authentication.
        
        Args:
            authorization_header (str):
            The Authorization header string.
        
        Returns:
            str: The Base64 part of the Authorization header,
            or None if not found.
        """
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[1]
