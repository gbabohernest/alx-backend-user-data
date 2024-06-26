#!/usr/bin/env python3
"""
This module defines an BasicAuth class that inherits from Auth class.
"""

from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import base64


class BasicAuth(Auth):
    """Class for basic authentication."""

    def extract_base64_authorization_header(self, authorization_header: str
                                            ) -> str:
        """ Extract the Base64 part of the Authorization
            header for Basic Authentication.
        """
        if authorization_header is None or not \
                isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        # Extract the Base64 part after 'Basic ' which is 6 chars long
        base64_part = authorization_header.split('Basic ')[1]
        return base64_part if base64_part.strip() else None

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """ Decode the Base64 authorization header
             and return the decoded value.
         """
        if base64_authorization_header is None or not \
                isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_str = decoded_bytes.decode('utf-8')
            return decoded_str

        except (base64.binascii.Error, UnicodeDecodeError):
            pass
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """ Extract the user email and password from
            the decoded Base64 authorization header.
        """
        if decoded_base64_authorization_header is None or not \
                isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        # user_email, user_password = decoded_base64_authorization_header \
        #    .split(':')

        user_data = decoded_base64_authorization_header.split(':', 1)
        user_email = user_data[0]
        user_password = user_data[1] if len(user_data) > 1 else ''

        return user_email, user_password

    def user_object_from_credentials(self, user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """ Return the User instance based on email and password. """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({'email': user_email})
            if not users or len(users) == 0:
                return None

            # user = users[0]
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user

            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Retrieve the User instance for a request using
            Basic Authentication.
        """
        if request is None:
            return None

        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return None

        base64_header = self.extract_base64_authorization_header(auth_header)
        if base64_header is None:
            return None

        decoded_header = self.decode_base64_authorization_header(base64_header)
        if decoded_header is None:
            return None

        user_email, user_password = self.extract_user_credentials(
            decoded_header)

        if user_email is None or user_password is None:
            return None

        return self.user_object_from_credentials(user_email, user_password)
