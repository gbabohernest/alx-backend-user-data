#!/usr/bin/env python3
"""DB module
"""

from sqlalchemy import create_engine, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
# from sqlalchemy.exc import IntegrityError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The user object representing the added user.
        """

        user = None

        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()

        except Exception:
            pass

        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user in the database based on input arguments.

        Args:
            **kwargs: Arbitrary keyword arguments representing filters
                      for the query.
        Returns:
            User: The User object matching the query.

        Raises:
            NoResultFound: If no user is found based on the input arguments.
            InvalidRequestsError: If invalid query arguments are passed.
        """

        try:
            query_filters = [getattr(User, key) == value for key, value in
                             kwargs.items() if hasattr(User, key)]
            if not query_filters:
                raise InvalidRequestError()

            result = (self._session.query(User).filter(and_(*query_filters))
                      .first())

            if result is None:
                raise NoResultFound()

            return result
        except NoResultFound:
            raise NoResultFound
        except InvalidRequestError:
            raise InvalidRequestError()
