from models import Base  # Importing the base class for SQLAlchemy models
from sqlalchemy.orm import relationship  # For defining relationships between models
from sqlalchemy.sql import func  # SQLAlchemy's SQL function library
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,  # Importing column types
)

class Event(Base):  # Event model class inheriting from Base
    """
    This is the Event model class. It defines the attributes and behaviors associated with
    an event in the application.
    """

    __tablename__ = "events"  # Specifying the table name in the database

    id = Column(Integer, primary_key=True, autoincrement=True)
    """
    The unique identifier for an event.
    """

    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    """
    The date and time when the event was created.
    """

    start_date = Column(DateTime())
    """
    The starting date and time of the event.
    """

    end_date = Column(DateTime())
    """
    The ending date and time of the event.
    """

    location = Column(String(50))
    """
    The location where the event will take place.
    """

    attendees_count = Column(Integer())
    """
    The number of attendees expected for the event.
    """

    notes = Column(String(1000))
    """
    Additional notes or comments about the event.
    """

    contract_id = Column(Integer, ForeignKey("contracts.id"))
    """
    Foreign key linking the event to a contract in the 'contracts' table.
    """

    support_contact_id = Column(Integer, ForeignKey("employees.id"))
    """
    Foreign key linking the event to an employee in the 'employees' table.
    """

    contract = relationship("Contract")
    """
    Establishing a relationship with the Contract model for easier navigation.
    """

    support_contact = relationship(
        "Employee",
    )
    """
    Establishing a relationship with the Employee model for easier navigation.
    """
