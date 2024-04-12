#!/usr/bin/env python3
"""
api/v1/auth/basic_auth.py
"""


from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """ BasicAuth class for managing basic authentication.
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extracts the Base64 part of the Authorization
        header for Basic Authentication.

        Args:
            authorization_header (str):
            The Authorization header string.

        Returns:
            str: The Base64 part of the Authorization header,
            or None if not found.
        """
        if ((authorization_header is None)
                or (not isinstance(authorization_header, str))):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """Decode the Base64 authorization header.

        Args:
            base64_authorization_header (str):
            The Base64 authorization header string.

        Returns:
            str: The decoded value as UTF8 string,
            or None if decoding fails.
        """
        if base64_authorization_header is None or \
                not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except base64.binascii.Error:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """Extract user email and password from the Base64 decoded value.
        
        Args:
            decoded_base64_authorization_header (str):
            The Base64 decoded authorization header string.
        
        Returns:
            tuple: A tuple containing user email and password,
            or (None, None) if extraction fails.
        """
        if decoded_base64_authorization_header is None or \
                not isinstance(decoded_base64_authorization_header, str) or \
                ':' not in decoded_base64_authorization_header:
            return None, None
        
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password
    