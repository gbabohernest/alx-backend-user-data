#!/usr/bin/env python3
""" Defines a SessionAuth class for session-based authentication.
"""

from api.v1.auth.auth import Auth
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

    def user_id_for_session(self, session_id: str = None) -> str:
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
