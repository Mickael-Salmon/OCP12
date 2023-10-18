from models import Base  # Importing the base class for SQLAlchemy models
from sqlalchemy.orm import relationship  # For defining relationships between models
from sqlalchemy.sql import func  # SQLAlchemy's SQL function library
from sqlalchemy import (
    Column,
    Integer,
    Float,
    DateTime,
    Boolean,
    ForeignKey,  # Importing column types
)

class Contract(Base):  # Contract model class inheriting from Base
    """
    This is the Contract model class. It defines the attributes and behaviors associated with
    a contract in the application.
    """

    __tablename__ = "contracts"  # Specifying the table name in the database

    id = Column(Integer, primary_key=True, autoincrement=True)
    """
    The unique identifier for a contract.
    """

    total_amount = Column(Float(precision=2))
    """
    The total amount of the contract with a floating-point precision of 2.
    """

    to_be_paid = Column(Float(precision=2))
    """
    The amount yet to be paid on the contract with a floating-point precision of 2.
    """

    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    """
    The date and time when the contract was created.
    """

    is_signed = Column(Boolean())
    """
    A flag indicating whether the contract has been signed or not.
    """

    client_id = Column(Integer, ForeignKey("clients.id"))
    """
    Foreign key linking the contract to a client in the 'clients' table.
    """

    account_contact_id = Column(Integer, ForeignKey("employees.id"))
    """
    Foreign key linking the contract to an employee in the 'employees' table.
    """

    client = relationship(
        "Client",
    )
    """
    Establishing a relationship with the Client model for easier navigation.
    """

    account_contact = relationship(
        "Employee",
    )
    """
    Establishing a relationship with the Employee model for easier navigation.
    """
