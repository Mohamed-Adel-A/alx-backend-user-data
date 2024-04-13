#!/usr/bin/env python3
"""
Auth module
"""
from db import DB
from user import User
import bcrypt
import uuid


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """
        Hashes a password
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user
        """
        if self._db.find_user_by(email=email):
            raise ValueError(f"User {email} already exists")
        hashed_password = self._hash_password(password)
        return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates user login
        """
        user = self._db.find_user_by(email=email)
        if user and bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
            return True
        return False

    def _generate_uuid(self) -> str:
        """
        Generates a UUID
        """
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """
        Creates a session for a user
        """
        user = self._db.find_user_by(email=email)
        if not user:
            return None
        session_id = self._generate_uuid()
        user.session_id = session_id
        self._db._session.commit()
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Gets user from session ID
        """
        return self._db.find_user_by(session_id=session_id)

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys user session
        """
        user = self._db.find_user_by(id=user_id)
        if user:
            user.session_id = None
            self._db._session.commit()
