"""
This file defines the Manager class, which serves as an abstract base class for all other model-specific manager classes.
The Manager class provides generic methods for CRUD operations and is intended to be subclassed by other managers that handle specific models.
"""
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import sqlalchemy
import typing

from authentification.environ import DATABASE_PASSWORD, DATABASE_USERNAME
from models import Base
from models.employees import Employee
from models.clients import Client
from models.contracts import Contract
from models.events import Event


# Initialize the database engine
engine = sqlalchemy.create_engine(
    f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@localhost/EpicEvents"
)


def drop_tables():
    """
    Drop all database tables.
    """
    # Perform the table drop operation
    Base.metadata.drop_all(engine)


def create_tables():
    """
    Create all database tables from the declared and imported models.
    """
    # Perform the table creation operation
    Base.metadata.create_all(engine)


class Manager(ABC):
    """
    Abstract base class template to implement model managers.
    Provides generic methods for CRUD operations that are intended to be overridden by subclasses.
    """

    def __init__(self, session: Session, model: type) -> None:
        """
        Initialize the Manager with a database session and a model type.
        """
        self._session = session
        self._model = model

    def create(self, obj):
        """
        Create a new record in the database.
        """
        try:
            # Add and commit the new object to the database
            self._session.add(obj)
            self._session.commit()

            return obj

        except IntegrityError as e:
            # Handle IntegrityError exceptions
            print(f"Integrity error : {e._message()}")

        except Exception as e:
            # Handle other exceptions
            print(f"Unhandled exception: {type(e).__name__}")

        return None

    def all(self):
        """
        Retrieve all records of the model from the database.
        """
        request = sqlalchemy.select(self._model)
        return self._session.scalars(request).all()

    def get(self, where_clause):
        """
        Retrieve records that match the given condition from the database.
        """
        request = sqlalchemy.select(self._model).where(where_clause)
        return self._session.scalars(request).all()

    @abstractmethod
    def update(self, *args, **kwargs):
        """
        Abstract method for updating records.
        To be implemented by subclasses.
        """
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        """
        Abstract method for deleting records.
        To be implemented by subclasses.
        """
        pass
