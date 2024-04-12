#!/usr/bin/env python3
"""Using bcrypt, this module defines a
   function that encrypt a password and
   return a salted, hashed password.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt and
       return the hashed password as bytes
    """
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password
