#!/usr/bin/env python3
"""
Auth module
"""
from db import DB
from user import User
import bcrypt
import uuid
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """Generate a UUID and return its string representation"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user
        """
        # Check if user already exists
        try:
            existing_user = self._db.find_user_by(email=email)
        except NoResultFound:
            # Hash the password
            hashed_password = _hash_password(password)

            # Add user to the database
            user = self._db.add_user(
                email=email,
                hashed_password=hashed_password)

            return user

        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user credentials"""
        user = None
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(
                    password.encode("utf-8"),
                    user.hashed_password,
                )
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """Create a new session for the user"""
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if user is None:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """Retrieve user from session ID"""
        if not session_id:
            return None

        user = None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user
