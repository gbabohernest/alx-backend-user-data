#!/usr/bin/env python3
"""
This module defines an Auth class that manage API authentication.
"""
from typing import List, TypeVar
# from flask import request
from os import getenv


class Auth:
    """ Class to manage API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if authentication is required for a given path.

        Args:
            path: (str): The endpoint path being accessed.
            excluded_paths: (List[str]): List of paths that do not require
                            authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """

        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        path = path.rstrip('/')
        excluded_paths = [p.rstrip('/') for p in excluded_paths]

        for excluded_path in excluded_paths:
            # slash tolerant comparison
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Get the authorization header from the request.

        Args:
            request (flask.Request): The Flask request object (optional).

        Returns:
            str: The authorization header value, or None if not found.
        """

        if request is None:
            return None

        if 'Authorization' not in request.headers:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Get the current authenticated user.

        Args:
            request (flask.Request): The Flask request object (optional).

        Returns:
            TypeVar('User'): The current user object, or None if
                             not authenticated.
        """
        # return request
        return None

    def session_cookie(self, request=None):
        """
        Retrieve a cookie value from a request.

        Args:
            request(flask.request): The flask request object (optional).

        Returns:
            str: The value of the specified cookie if found, None otherwise.
        """
        if request is None:
            return None
        else:
            session_name = getenv('SESSION_NAME', '_my_session_id')
            return request.cookies.get(session_name)
