"""
This file defines the Contract model, which represents a contract entity in the application.
The model includes various fields like total_amount, to_be_paid, and is_signed, among others.
It specifies the relationships with the 'Client' and 'Employee' models through the 'client_id' and 'account_contact_id' fields, respectively.
"""
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
from sqlalchemy.orm import validates
class Contract(Base):  # Contract model class inheriting from Base
    """
    This is the Contract model class. It defines the attributes and behaviors associated with
    a contract in the application.

    Attributes:
        id (int): The unique identifier for a contract.
        total_amount (float): The total amount of the contract with a floating-point precision of 2.
        to_be_paid (float): The amount yet to be paid on the contract with a floating-point precision of 2.
        creation_date (datetime): The date and time when the contract was created.
        is_signed (bool): A flag indicating whether the contract has been signed or not.
        client_id (int): Foreign key linking the contract to a client in the 'clients' table.
        account_contact_id (int): Foreign key linking the contract to an employee in the 'employees' table.
        client (Client): Relationship with the Client model for easier navigation.
        account_contact (Employee): Relationship with the Employee model for easier navigation.

    Methods:
        validate_amounts(key, amount): Validate that the amounts are positive and to_be_paid does not exceed total_amount.
        list_contracts(): Retrieve a list of all contracts and print their details.

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
    @validates('total_amount', 'to_be_paid')
    def validate_amounts(self, key, amount):
        """
        Validate that the amounts are positive and to_be_paid does not exceed total_amount.

        Parameters:
        - key (str): The key representing the amount being validated.
        - amount (int or float): The amount to be validated.

        Raises:
        - ValueError: If the amount is not a positive number or if to_be_paid exceeds total_amount.

        Returns:
        - amount (int or float): The validated amount.
        """
        if not isinstance(amount, (int, float)) or amount < 0:
            raise ValueError(f"{key} must be a positive number")
        if key == 'to_be_paid' and amount > self.total_amount:
            raise ValueError("to_be_paid cannot exceed total_amount")
        return amount
    """
    Establishing a relationship with the Employee model for easier navigation.
    """
    def list_contracts(self):
            """
            Retrieve a list of all contracts and print their details.

            Returns:
                list: A list of Contract objects.
            """
            contracts = self.session.query(Contract).all()
            self.console.print("[bold green]Liste des contrats :[/bold green]")
            for contract in contracts:
                client_name = contract.client.full_name if contract.client else "Client inconnu"
                self.console.print(f"{contract.id} : {client_name} - {contract.total_amount} - {'Signé' if contract.is_signed else 'Non signé'}")
            return contracts
