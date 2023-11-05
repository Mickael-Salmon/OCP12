"""
This file defines the Client model, which represents a client entity in the application.
The model includes various fields like full_name, email, phone, and enterprise, among others.
It also specifies the relationship with the 'Employee' model through the 'sales_contact_id' field.
"""
from models import Base  # Importing the base class for SQLAlchemy models
from sqlalchemy.orm import relationship  # ORM package for creating relationships between tables
from sqlalchemy.sql import func  # SQLAlchemy's SQL function library
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Boolean,
)  # Importing column types and ForeignKey for creating table schema

class Client(Base):  # Client model class inheriting from Base
    """
    This is the Client model class. It describes the attributes and behaviors associated with
    a client in the application.
    """

    __tablename__ = "clients"  # Specifying the table name in the database

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )  # An integer field 'id' which is also the primary key and auto-incremented
    """
    The unique identifier for a client.
    """

    full_name = Column(String(50), nullable=False)  # A string field 'full_name' which is not nullable
    """
    The full name of the client.
    """

    email = Column(
        String(50),
        nullable=False,
        unique=True,
    )  # A string field 'email' which is unique and not nullable
    """
    The email address of the client. Must be unique.
    """

    phone = Column(
        String(15),
        nullable=False,
        unique=True,
    )  # A string field 'phone' which is unique and not nullable
    """
    The phone number of the client. Must be unique.
    """

    enterprise = Column(String(50))  # A string field 'enterprise'
    """
    The name of the enterprise that the client belongs to.
    """

    creation_date = Column(DateTime(timezone=True), server_default=func.now())  # A datetime field 'creation_date' with a default value
    """
    The date and time when the client record was created.
    """

    last_update = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )  # A datetime field 'last_update' that updates itself each time the record is updated
    """
    The date and time when the client record was last updated.
    """

    sales_contact_id = Column(Integer, ForeignKey("employees.id"), nullable=False)  # A foreign key linking to the 'employees' table
    """
    The ID of the sales contact (Employee) responsible for this client.
    """

    sales_contact = relationship(
        "Employee",
    )  # ORM relationship to the Employee model
    """
    This establishes an ORM relationship between Client and Employee, allowing us to access
    the Employee model when we have a Client object.
    """
    is_active = Column(Boolean, default=True)