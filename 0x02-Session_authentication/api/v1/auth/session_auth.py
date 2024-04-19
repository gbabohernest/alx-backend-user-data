#!/usr/bin/env python3
""" Defines a SessionAuth class for session-based authentication.
"""

from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """ Class for session-based authentication.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a Session ID for a user_id.

        Args:
            user_id (str): The user ID for which to create a session.
        Returns:
            str: The session ID if successful, None otherwise.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieve a User ID based on a Session ID.

        Args:
            session_id (str): The session ID for which to retrieve
            the user ID.
        Returns:
            str: The user ID associated with the session ID if
            found, else None.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Retrieve the current authenticated user based on a cookie value.

        Args:
            request (flask.Request): The Flask request object (optional).

        Returns:
            User: The User instance associated with the current session
            if authenticated, None otherwise.
        """
        if request is None:
            return None

        session_id = self.session_cookie(request)
        if session_id is None:
            return None

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None

        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """
        Delete the user session and logout.

        Args:
            request (flask.Request): The Flask request object
            containing the session ID cookie.

        Returns:
            bool: True if the session was successfully destroyed,
            False otherwise.
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
            return True

        return False
