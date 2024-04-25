#!/usr/bin/env python3
"""Defines a SQLAlchemy model representing a User in the database.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    SQLAlchemy model representing a User in the database.

    Attributes:
        id (int): The integer primary key.
        email (str): A non-nullable string representing the user's email
        hashed_password (str): A non-nullable string representing the hashed
                               password
        session_id (str): A nullable string representing the user's session ID.
        reset_token (str): A nullable string representing the user's reset
                           token.
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
