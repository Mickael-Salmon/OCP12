"""
This file defines the Client model, which represents a client entity in the application.
The model includes various fields like full_name, email, phone, and enterprise, among others.
It also specifies the relationship with the 'Employee' model through the 'sales_contact_id' field.
"""
from models import Base  # Importing the base class for SQLAlchemy models
from sqlalchemy.orm import relationship, validates  # ORM package for creating relationships between tables and validation
from sqlalchemy.sql import func  # SQLAlchemy's SQL function library
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Boolean,
)  # Importing column types and ForeignKey for creating table schema
from sqlalchemy.exc import IntegrityError  # Importing exception class for handling integrity errors

import re  # Regular expression library for validation patterns

class Client(Base):  # Client model class inheriting from Base
    """
    This is the Client model class. It describes the attributes and behaviors associated with
    a client in the application.
    """

    __tablename__ = "clients"  # Specifying the table name in the database

    id = Column(Integer, primary_key=True, autoincrement=True)
    """
    The unique identifier for a client.
    """

    full_name = Column(String(50), nullable=False)
    """
    The full name of the client.
    """

    email = Column(String(50), nullable=False, unique=True)
    """
    The email address of the client. Must be unique.
    """

    phone = Column(String(15), nullable=False, unique=True)
    """
    The phone number of the client. Must be unique.
    """

    enterprise = Column(String(50))
    """
    The name of the enterprise that the client belongs to.
    """

    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    """
    The date and time when the client record was created.
    """

    last_update = Column(DateTime(timezone=True), onupdate=func.now())
    """
    The date and time when the client record was last updated.
    """

    sales_contact_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    """
    The ID of the sales contact (Employee) responsible for this client.
    """

    sales_contact = relationship("Employee")
    """
    This establishes an ORM relationship between Client and Employee, allowing us to access
    the Employee model when we have a Client object.
    """

    is_active = Column(Boolean, default=True)
    """
    Indicates whether the client is active or not.
    """

    @validates('email')
    def validate_email(self, key, email):
        """
        Validate the format of the email address.
        """
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError(f"Invalid email address: {email}")
        return email

    @validates('phone')
    def validate_phone(self, key, phone):
        """
        Validate the format of the phone number.
        """
        if not re.match(r"^\+?\d{10,15}$", phone):
            raise ValueError(f"Invalid phone number: {phone}")
        return phone

    # Add a method to handle insertion and update operations with error handling
    def insert_or_update(self, session):
        """
        Insert or update a client record with error handling for integrity issues.
        """
        try:
            session.add(self)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise ValueError(f"An error occurred while inserting/updating the record: {e.orig}")
