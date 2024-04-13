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

        # Retrieve the UserSession from the database using the session_id
        session = UserSession.get(session_id)

        # If session is found and session is not expired
        if session:
            # Check if the session is expired
            session_created_at = session.created_at
            session_duration = self.session_duration
            current_time = datetime.now()
            if (current_time - session_created_at).total_seconds() <= session_duration:
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
