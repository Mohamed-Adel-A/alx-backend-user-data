#!/usr/bin/env python3
"""
user session module
"""
from sqlalchemy import Column, String, ForeignKey
from models.base import Base

class UserSession(Base):
    """UserSession model for storing session IDs in the database."""

    __tablename__ = 'user_sessions'

    id = Column(String(60), primary_key=True)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
