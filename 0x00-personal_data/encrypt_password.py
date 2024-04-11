"""
enccrypt_password
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash a password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validate a password against its hashed version.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)


if __name__ == "__main__":
    password = "MyAmazingPassw0rd"
    hashed_password = hash_password(password)
    print(hashed_password)
    print(is_valid(hashed_password, password))
