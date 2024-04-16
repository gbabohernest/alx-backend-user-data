#!/usr/bin/env python3
"""
This module defines an BasicAuth class that inherits from Auth class.
"""

from api.v1.auth.auth import Auth


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
