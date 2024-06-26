#!/usr/bin/env python3
"""
SessionDBAuth module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """Session authentication with session IDs stored in the database."""

    def create_session(self, user_id=None):
        """Create a new session and store it in the database."""
        session_id = super().create_session(user_id)
        if session_id:
            new_session = UserSession(session_id=session_id, user_id=user_id)
            new_session.save()
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """Retrieve user ID for a session ID from the database."""
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        cur_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        exp_time = sessions[0].created_at + time_span
        if exp_time < cur_time:
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None):
        """Destroy a session by removing it from the database."""
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        sessions[0].remove()
        return True
