#!/usr/bin/env python3
"""
This module defines an BasicAuth class that inherits from Auth class.
"""

from api.v1.auth.auth import Auth
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

        user_email, user_password = decoded_base64_authorization_header \
            .split(':')
        return user_email, user_password
