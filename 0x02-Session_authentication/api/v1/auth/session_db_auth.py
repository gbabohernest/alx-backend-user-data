#!/usr/bin/env python3
""" Session DB Authentication module
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta
from typing import TypeVar, Optional


class SessionDBAuth(SessionExpAuth):
    """ Session Authentication with Database class
    """

    def create_session(self, user_id=None) -> Optional[str]:
        """ Create and store a new instance of UserSession.
        """
        if user_id is None:
            return None

        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        # store the UserSession in the database (file)
        session_data = {
            'user_id': user_id,
            'session_id': session_id,
            # 'created_at': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
            # 'updated_at': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        }

        user_session = UserSession(**session_data)
        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None) -> Optional[str]:
        """ Get the User ID of the user associated
            with a given session ID from the database.
        """
        # if session_id is None:
        #     return None
        #
        # # search for the UserSession based on session_id
        # user_sessions = UserSession.search({'session_id': session_id})
        # if not user_sessions:
        #     return None
        #
        # return user_sessions[0].user_id

        if session_id is None:
            return None

        try:
            # search for the UserSession based on session_id
            user_sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None

        if not user_sessions:
            return None

        cur_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        exp_time = user_sessions[0].created_at + time_span

        if exp_time < cur_time:
            # Session has expired
            user_sessions[0].remove()
            return None

        return user_sessions[0].user_id

    def destroy_session(self, request=None) -> bool:
        """ Destroy the UserSession based on Session ID
           from request cookie
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        # Delete the UserSession from the database
        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return False

        user_sessions[0].remove()
        return True
