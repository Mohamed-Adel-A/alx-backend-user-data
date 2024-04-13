#!/usr/bin/env python3
"""
SessionExpAuth module
"""

from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session-based authentication with expiration."""

    def __init__(self):
        """Initialize SessionExpAuth."""
        super().__init__()
        # Assign session_duration based on SESSION_DURATION env variable
        self.session_duration = int(os.getenv('SESSION_DURATION', 0))

    def create_session(self, user_id=None):
        """Create a session ID with expiration."""
        # Create session ID using SessionAuth's create_session method
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        # Store session ID and creation time in user_id_by_session_id
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve user ID for a session ID with expiration."""
        if session_id is None:
            return None
        # Check if session ID exists and retrieve user ID
        session_data = self.user_id_by_session_id.get(session_id)
        if session_data is None:
            return None
        user_id = session_data.get('user_id')
        created_at = session_data.get('created_at')
        if self.session_duration <= 0 or created_at is None:
            return user_id
        # Check session expiration based on session_duration
        if created_at is None:
            return None
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None
        return user_id
