#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from user import User

Base = declarative_base()


class DB:
    """
    DB class
    """

    def __init__(self) -> None:
        """
        Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """
        Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email, hashed_password):
        """
        Add user to the database
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs):
        """
        Find user by attribute
        """
        return self._session.query(User).filter_by(**kwargs).first()

    def update_user(self, user_id, **kwargs):
        """
        Update user by ID
        """
        user = self.find_user_by(id=user_id)
        if not user:
            raise ValueError("User not found")
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError("Invalid attribute")
        self._session.commit()
