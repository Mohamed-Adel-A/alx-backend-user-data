from flask import request
from typing import List, TypeVar

class Auth:
    """ Auth class for managing API authentication.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method to check if authentication is required for a given path.

        Args:
            path (str): The requested path.
            excluded_paths (List[str]): List of paths that are excluded from authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
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
