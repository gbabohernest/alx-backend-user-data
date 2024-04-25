#!/usr/bin/env python3
"""
A model for authentications related processes.
"""

import bcrypt
from sqlalchemy.orm.exc import NoResultFound


from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    Generate a salted hash of the input password
    using bcrypt.hashpw.

    Args:
        password (str): The password string to hash.

    Returns:
        bytes: The salted hash of the input password.
    """

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database
    """

    def __init__(self):
        """Initialize"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user in the database.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The User object of the newly registered user.

        Raises:
            ValueError: If a user with the same email already exists.
        """

        try:
            # check if user with the same email already exists
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists.")
        except NoResultFound:
            hashed_password = _hash_password(password)

            new_user = self._db.add_user(email, str(hashed_password))

            return new_user
