#!/usr/bin/env python3
""" Defines a  Class for session-based authentication
    with session expiration.
"""

from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth
import os


class SessionExpAuth(SessionAuth):
    """Class for session-based authentication with session expiration."""

    def __init__(self):
        """Initialize SessionExpAuth instance."""
        super().__init__()
        self.session_duration = int(os.getenv("SESSION_DURATION", 0))

    def create_session(self, user_id=None):
        """
        Create a session ID and associate it with user details.

        Args:
            user_id (str): User ID for whom the session is created.

        Returns:
            str: Session ID created or None if session creation fails.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dict = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Get the user ID associated with a session ID,
        considering session expiration.

        Args:
            session_id (str): Session ID to retrieve user ID.

        Returns:
            str: User ID associated with the session ID or None
            if session is expired or invalid.
        """
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None

        session_dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dict["user_id"]

        if "created_at" not in session_dict:
            return None

        created_at = session_dict["created_at"]
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None

        return session_dict["user_id"]
