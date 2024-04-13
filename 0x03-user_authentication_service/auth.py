#!/usr/bin/env python3
"""
Auth module
"""
from db import DB
from user import User
import bcrypt
import uuid


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
