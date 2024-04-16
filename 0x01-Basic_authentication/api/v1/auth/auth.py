#!/usr/bin/env python3
"""
This module defines an Auth class that manage API authentication.
"""
from typing import List, TypeVar
from flask import request


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

        for excluded_path in excluded_paths:
            # slash tolerant comparison
            if path.rstrip('/') == excluded_path.rstrip('/'):
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
        return request

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Get the current authenticated user.

        Args:
            request (flask.Request): The Flask request object (optional).

        Returns:
            TypeVar('User'): The current user object, or None if
                             not authenticated.
        """
        return request
