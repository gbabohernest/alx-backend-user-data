#!/usr/bin/env python3
"""
A model for authentications related processes.
"""

import uuid
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


def _generate_uuid() -> str:
    """
    Generate a new UUID and return its string representation.

    Returns:
        str: The string representation of the new UUID.
    """
    return str(uuid.uuid4())


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

            new_user = self._db.add_user(email, hashed_password)

            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Check if the login credentials are valid.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            bool: True if the login credentials are valid, False otherwise.
        """

        try:
            user = self._db.find_user_by(email=email)
            if not user:
                return False

            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)

        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Create a new session for the user and return
        the session ID.

        Args:
            email (str): The email of the user.

        Returns:
            str: The session ID.
        """
        try:
            user = self._db.find_user_by(email=email)

            if not user:
                return None

            session_id = _generate_uuid()
            user.session_id = session_id

            return user.session_id

        except NoResultFound:
            return None
