"""
This file defines the Manager class, which serves as an abstract base class for model-specific managers.
The Manager class provides generic CRUD operations and is meant to be subclassed by other managers.

The Manager class provides the following methods:
- create(obj): Create a new record in the database.
- all(): Retrieve all records of the model from the database.
- get(where_clause): Retrieve records that match the given condition from the database.
- update(*args, **kwargs): Abstract method for updating records to be implemented by subclasses.
- delete(*args, **kwargs): Abstract method for deleting records to be implemented by subclasses.
"""
"""
This file defines the Manager class, which serves as an abstract base class for model-specific managers.
The Manager class provides generic CRUD operations and is meant to be subclassed by other managers.
"""

from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from accesscontrol.env_variables import DATABASE_PASSWORD, DATABASE_USERNAME
from models import Base
from sqlalchemy import create_engine
import sqlalchemy

# Initialize the database engine
engine = create_engine(f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@localhost/epic_events")

def drop_tables():
    """ Drop all database tables. """
    Base.metadata.drop_all(engine)

def create_tables():
    """ Create all database tables from the declared models. """
    Base.metadata.create_all(engine)

class Manager(ABC):
    """ Abstract base class for implementing model managers with CRUD operations. """

    def __init__(self, session: Session, model: type) -> None:
        self._session = session
        self._model = model

    def create(self, obj):
        """ Create a new record in the database. """
        try:
            self._session.add(obj)
            self._session.commit()
            return obj
        except IntegrityError as e:
            self._session.rollback()
            # Log the integrity error
            print(f"Integrity error: {e.orig}")
        except SQLAlchemyError as e:
            self._session.rollback()
            # Log other SQL Alchemy exceptions
            print(f"SQLAlchemy error: {e.orig}")
        return None

    def all(self):
        """ Retrieve all records of the model from the database. """
        request = sqlalchemy.select(self._model)
        return self._session.scalars(request).all()

    def get(self, where_clause):
        """ Retrieve records that match the given condition from the database. """
        request = sqlalchemy.select(self._model).where(where_clause)
        return self._session.scalars(request).all()

    @abstractmethod
    def update(self, *args, **kwargs):
        """ Abstract method for updating records to be implemented by subclasses. """
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        """ Abstract method for deleting records to be implemented by subclasses. """
        pass
