#!/usr/bin/env python3
"""
A model for authentications related processes.
"""

import bcrypt


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
