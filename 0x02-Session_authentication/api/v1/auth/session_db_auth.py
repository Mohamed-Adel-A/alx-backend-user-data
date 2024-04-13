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
            new_session = UserSession(id=session_id, user_id=user_id)
            new_session.save()
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """Retrieve user ID for a session ID from the database."""
        if session_id is None:
            return None
        user_id = super().user_id_for_session_id(session_id)
        if user_id:
            session = UserSession.get(session_id)
            if session:
                return session.user_id
        return None

    def destroy_session(self, request=None):
        """Destroy a session by removing it from the database."""
        session_id = self.session_cookie(request)
        if session_id:
            session = UserSession.get(session_id)
            if session:
                session.delete()
                return True
        return False
